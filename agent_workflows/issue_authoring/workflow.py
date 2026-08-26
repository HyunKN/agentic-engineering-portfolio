"""Implementation for validated AI-authored GitHub Issue drafts."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Callable, Iterable, Mapping, Sequence

from agent_workflows.publication_safety import find_publication_risks


TITLE_PARENT_RE = re.compile(r"^\[(M[0-5])\]\s+(.+)$")
TITLE_WORK_RE = re.compile(
    r"^\[(M[0-5])-(\d{3})\]\[([A-Z][A-Z0-9-]{2,})\]\s+(.+)$"
)
HANGUL_RE = re.compile(r"[가-힣]")
CHECKBOX_RE = re.compile(r"- \[[ xX]\]")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ALLOWED_LABELS = frozenset(
    {
        "track:foundation",
        "track:localtwin",
        "track:landmark",
        "track:portfolio",
        "type:implementation",
        "type:experiment",
        "type:evaluation",
        "type:research",
        "type:docs",
        "type:infra",
        "type:decision",
        "priority:p0",
        "priority:p1",
        "priority:p2",
        "priority:p3",
        "risk:public-write",
        "risk:cost",
        "risk:privacy",
        "risk:fixture-leakage",
        "needs:user-action",
    }
)
REQUIRED_KEYS = frozenset(
    {"version", "repository", "kind", "title", "body", "labels", "milestone"}
)
OPTIONAL_KEYS = frozenset({"issue_number", "parent_issue"})
REQUIRED_WORK_HEADINGS = ("목표", "작업 범위", "완료 기준", "검증 계획")


class DraftValidationError(ValueError):
    """Raised when one or more Issue draft invariants fail."""

    def __init__(self, source: Path, errors: Sequence[str]) -> None:
        self.source = source
        self.errors = tuple(errors)
        detail = "\n".join(f"- {error}" for error in self.errors)
        super().__init__(f"{source}: Issue draft validation failed\n{detail}")


@dataclass(frozen=True)
class IssueDraft:
    """A validated Issue draft ready for preview or publication."""

    source: Path
    version: int
    repository: str
    kind: str
    title: str
    body: str
    labels: tuple[str, ...]
    milestone: str
    issue_number: int | None = None
    parent_issue: int | None = None

    @property
    def action(self) -> str:
        return "update" if self.issue_number is not None else "create"


def normalize_body(body: str) -> str:
    """Return stable LF Markdown with trailing whitespace removed."""

    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    return "\n".join(lines).strip() + "\n"


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _validate_mapping(data: Mapping[str, Any], source: Path) -> IssueDraft:
    errors: list[str] = []
    keys = set(data)
    missing = sorted(REQUIRED_KEYS - keys)
    unknown = sorted(keys - REQUIRED_KEYS - OPTIONAL_KEYS)
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")

    version = data.get("version")
    repository = data.get("repository")
    kind = data.get("kind")
    title = data.get("title")
    raw_body = data.get("body")
    labels = data.get("labels")
    milestone = data.get("milestone")
    issue_number = data.get("issue_number")
    parent_issue = data.get("parent_issue")

    if version != 1:
        errors.append("version must be 1")
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        errors.append("repository must use owner/name format")
    if kind not in {"parent", "work", "experiment"}:
        errors.append("kind must be parent, work, or experiment")
    if not isinstance(title, str) or not title.strip() or "\n" in title:
        errors.append("title must be one non-empty line")
        title = ""
    if not isinstance(raw_body, str) or not raw_body.strip():
        errors.append("body must be a non-empty Markdown string")
        raw_body = ""
    if not isinstance(labels, list) or not labels or not all(
        isinstance(label, str) and label for label in labels
    ):
        errors.append("labels must be a non-empty string array")
        labels = []
    if not isinstance(milestone, str) or not milestone.strip():
        errors.append("milestone must be a non-empty string")
        milestone = ""
    if issue_number is not None and not _positive_int(issue_number):
        errors.append("issue_number must be a positive integer when present")
    if parent_issue is not None and not _positive_int(parent_issue):
        errors.append("parent_issue must be a positive integer when present")
    if issue_number is not None and issue_number == parent_issue:
        errors.append("an Issue cannot be its own parent")

    body = normalize_body(raw_body)

    if title and not HANGUL_RE.search(title):
        errors.append("title must include a Korean description")
    if body and not HANGUL_RE.search(body):
        errors.append("body must be written primarily for Korean review")

    phase = ""
    if kind == "parent":
        match = TITLE_PARENT_RE.fullmatch(title)
        if not match:
            errors.append("parent title must match '[M0] 한국어 제목'")
        else:
            phase = match.group(1)
            if not re.search(rf"(?m)^## {re.escape(phase)}(?:\s|$)", body):
                errors.append(f"parent body must contain a '## {phase}' heading")
    elif kind in {"work", "experiment"}:
        match = TITLE_WORK_RE.fullmatch(title)
        if not match:
            errors.append(
                "work title must match '[M0-010][TASK-ID] 한국어 제목'"
            )
        else:
            phase = match.group(1)
            order = int(match.group(2))
            task_id = match.group(3)
            if order == 0 or order % 5 != 0:
                errors.append("Order must be a positive 5-step value such as 010 or 015")
            if kind == "experiment" and "EXP" not in task_id:
                errors.append("experiment Task ID must contain EXP")
        for heading in REQUIRED_WORK_HEADINGS:
            if not re.search(rf"(?m)^## {re.escape(heading)}\s*$", body):
                errors.append(f"body is missing required heading: ## {heading}")

    checkbox_matches = list(CHECKBOX_RE.finditer(body))
    if kind == "parent" and not checkbox_matches:
        errors.append("parent body must contain at least one checklist item")
    for match in checkbox_matches:
        if match.start() > 0 and body[match.start() - 1] != "\n":
            errors.append(
                "checklist markers must start on their own line; possible newline collapse"
            )
            break
    for line in body.splitlines():
        if CHECKBOX_RE.match(line) and not line[5:].strip():
            errors.append("checklist items must include text")
            break

    public_text = f"{title}\n{body}"
    errors.extend(f"draft {risk}" for risk in find_publication_risks(public_text))

    label_values = tuple(labels)
    if len(label_values) != len(set(label_values)):
        errors.append("labels must not contain duplicates")
    unknown_labels = sorted(set(label_values) - ALLOWED_LABELS)
    if unknown_labels:
        errors.append(f"unknown labels: {', '.join(unknown_labels)}")
    for prefix in ("track:", "type:", "priority:"):
        count = sum(label.startswith(prefix) for label in label_values)
        if count != 1:
            errors.append(f"labels must contain exactly one {prefix} label")

    if errors:
        raise DraftValidationError(source, errors)

    return IssueDraft(
        source=source,
        version=version,
        repository=repository,
        kind=kind,
        title=title.strip(),
        body=body,
        labels=label_values,
        milestone=milestone.strip(),
        issue_number=issue_number,
        parent_issue=parent_issue,
    )


def prepare_drafts(paths: Iterable[Path]) -> list[IssueDraft]:
    """Load and validate every JSON draft before any side effect is allowed."""

    drafts: list[IssueDraft] = []
    for path in paths:
        source = Path(path)
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise DraftValidationError(source, [str(error)]) from error
        items = payload if isinstance(payload, list) else [payload]
        if not items or not all(isinstance(item, dict) for item in items):
            raise DraftValidationError(
                source, ["JSON root must be an object or a non-empty object array"]
            )
        for index, item in enumerate(items):
            item_source = source if len(items) == 1 else Path(f"{source}#{index}")
            drafts.append(_validate_mapping(item, item_source))
    return drafts


def render_preview(drafts: Sequence[IssueDraft]) -> str:
    """Render a human-reviewable dry-run without touching GitHub."""

    blocks: list[str] = []
    for draft in drafts:
        target = (
            f"#{draft.issue_number}" if draft.issue_number is not None else "new Issue"
        )
        blocks.append(
            "\n".join(
                [
                    f"=== {draft.action.upper()} {draft.repository} {target} ===",
                    f"Title: {draft.title}",
                    f"Milestone: {draft.milestone}",
                    f"Labels: {', '.join(draft.labels)}",
                    f"Parent: {draft.parent_issue or '-'}",
                    "--- BODY ---",
                    draft.body.rstrip(),
                ]
            )
        )
    return "\n\n".join(blocks) + "\n"


Runner = Callable[..., subprocess.CompletedProcess[str]]


class GithubPublisher:
    """Publish validated drafts through gh without shell interpolation."""

    def __init__(self, runner: Runner = subprocess.run) -> None:
        self._runner = runner

    def _run(self, args: list[str], *, body: str | None = None) -> str:
        result = self._runner(
            args,
            input=body,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"command failed: {' '.join(args[:4])}: {message}")
        return result.stdout.strip()

    def publish_many(self, drafts: Sequence[IssueDraft]) -> list[str]:
        """Publish a prevalidated batch and verify title/body round trips."""

        results: list[str] = []
        for draft in drafts:
            results.append(self.publish(draft))
        return results

    def publish(self, draft: IssueDraft) -> str:
        """Create or update one Issue and return its URL."""

        if draft.issue_number is None:
            args = [
                "gh",
                "issue",
                "create",
                "--repo",
                draft.repository,
                "--title",
                draft.title,
                "--body-file",
                "-",
                "--milestone",
                draft.milestone,
            ]
            for label in draft.labels:
                args.extend(["--label", label])
            url = self._run(args, body=draft.body)
            try:
                issue_number = int(url.rstrip("/").rsplit("/", 1)[-1])
            except ValueError as error:
                raise RuntimeError(f"could not parse created Issue URL: {url}") from error
        else:
            issue_number = draft.issue_number
            args = [
                "gh",
                "issue",
                "edit",
                str(issue_number),
                "--repo",
                draft.repository,
                "--title",
                draft.title,
                "--body-file",
                "-",
                "--milestone",
                draft.milestone,
            ]
            for label in draft.labels:
                args.extend(["--add-label", label])
            self._run(args, body=draft.body)
            url = f"https://github.com/{draft.repository}/issues/{issue_number}"

        if draft.parent_issue is not None:
            self._run(
                [
                    "gh",
                    "issue",
                    "edit",
                    str(issue_number),
                    "--repo",
                    draft.repository,
                    "--parent",
                    str(draft.parent_issue),
                ]
            )

        self._verify_round_trip(draft, issue_number)
        return url

    def _verify_round_trip(self, draft: IssueDraft, issue_number: int) -> None:
        raw = self._run(
            [
                "gh",
                "issue",
                "view",
                str(issue_number),
                "--repo",
                draft.repository,
                "--json",
                "title,body,milestone,labels",
            ]
        )
        try:
            remote = json.loads(raw)
        except json.JSONDecodeError as error:
            raise RuntimeError("GitHub verification returned invalid JSON") from error

        mismatches: list[str] = []
        if remote.get("title") != draft.title:
            mismatches.append("title")
        if normalize_body(remote.get("body") or "") != draft.body:
            mismatches.append("body")
        remote_milestone = (remote.get("milestone") or {}).get("title")
        if remote_milestone != draft.milestone:
            mismatches.append("milestone")
        remote_labels = {label.get("name") for label in remote.get("labels") or []}
        if not set(draft.labels).issubset(remote_labels):
            mismatches.append("labels")
        if mismatches:
            raise RuntimeError(
                f"GitHub round-trip verification failed: {', '.join(mismatches)}"
            )
