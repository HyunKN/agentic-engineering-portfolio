"""Implementation for immutable, public-safe external review packets."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
from typing import Any, Mapping, Protocol, Sequence

from agent_workflows.publication_safety import find_publication_risks


PACKET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,80}$")
GITHUB_REPOSITORY_RE = re.compile(
    r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$"
)
HANGUL_RE = re.compile(r"[가-힣]")
ALLOWED_CATEGORIES = frozenset(
    {
        "context",
        "decision",
        "implementation",
        "test",
        "operation",
        "conversation",
        "evidence",
    }
)
DENIED_NAMES = frozenset(
    {".env", ".env.local", ".env.production", "credentials.json", "secrets.json"}
)
DENIED_SUFFIXES = frozenset({".key", ".pem", ".p12", ".pfx"})
REQUIRED_KEYS = frozenset(
    {
        "version",
        "packet_id",
        "title",
        "repository_url",
        "source_commit",
        "scope",
        "sources",
        "references",
        "review_questions",
        "known_gaps",
        "exclusions",
    }
)


class PacketValidationError(ValueError):
    """Raised when a packet spec or generated packet is unsafe or inconsistent."""

    def __init__(self, subject: str | Path, errors: Sequence[str]) -> None:
        self.subject = str(subject)
        self.errors = tuple(errors)
        details = "\n".join(f"- {error}" for error in self.errors)
        super().__init__(f"{self.subject}: evaluation packet validation failed\n{details}")


class SourceReader(Protocol):
    """Seam for resolving an immutable source revision and reading its files."""

    def resolve_commit(self, ref: str) -> str: ...

    def read_file(self, commit: str, path: str) -> bytes: ...


class GitSourceReader:
    """Production adapter that reads blobs from a local Git repository."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root).resolve()

    def _run(self, args: list[str]) -> bytes:
        result = subprocess.run(
            ["git", "-C", str(self.repository_root), *args],
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            message = result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(message or "git command failed")
        return result.stdout

    def resolve_commit(self, ref: str) -> str:
        raw = self._run(["rev-parse", "--verify", f"{ref}^{{commit}}"])
        commit = raw.decode("ascii", errors="strict").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise RuntimeError(f"Git returned an invalid commit: {commit}")
        return commit

    def read_file(self, commit: str, path: str) -> bytes:
        return self._run(["show", f"{commit}:{path}"])


@dataclass(frozen=True)
class SourceEntry:
    path: str
    category: str
    description: str


@dataclass(frozen=True)
class PacketSpec:
    packet_id: str
    title: str
    repository_url: str
    source_commit: str
    scope: str
    sources: tuple[SourceEntry, ...]
    references: tuple[Mapping[str, str], ...]
    review_questions: tuple[str, ...]
    known_gaps: tuple[str, ...]
    exclusions: tuple[Mapping[str, str], ...]
    canonical_json: bytes


@dataclass(frozen=True)
class PlannedFile:
    path: str
    content: bytes
    category: str
    source_path: str | None = None
    description: str | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content).hexdigest()


@dataclass(frozen=True)
class PacketPlan:
    packet_id: str
    title: str
    repository_url: str
    source_commit: str
    files: tuple[PlannedFile, ...]
    manifest: Mapping[str, Any]


def _safe_relative_path(value: Any, *, field: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} must be a non-empty repository-relative path")
        return ""
    path = PurePosixPath(value)
    lowered_parts = {part.lower() for part in path.parts}
    if path.is_absolute() or ".." in path.parts or ".git" in lowered_parts:
        errors.append(f"{field} must not be absolute, traverse parents, or enter .git")
    if "\\" in value or str(path) != value:
        errors.append(f"{field} must use normalized POSIX separators")
    if path.name.lower() in DENIED_NAMES or path.suffix.lower() in DENIED_SUFFIXES:
        errors.append(f"{field} is denied by the public evidence policy")
    return value


def _string_list(data: Any, field: str, errors: list[str]) -> tuple[str, ...]:
    if not isinstance(data, list) or not data or not all(
        isinstance(item, str) and item.strip() for item in data
    ):
        errors.append(f"{field} must be a non-empty string array")
        return ()
    return tuple(item.strip() for item in data)


def _object_list(
    data: Any,
    field: str,
    required: frozenset[str],
    errors: list[str],
) -> tuple[Mapping[str, str], ...]:
    if not isinstance(data, list) or not data:
        errors.append(f"{field} must be a non-empty object array")
        return ()
    items: list[Mapping[str, str]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict) or set(item) != required:
            errors.append(
                f"{field}[{index}] must contain exactly: {', '.join(sorted(required))}"
            )
            continue
        if not all(isinstance(item[key], str) and item[key].strip() for key in required):
            errors.append(f"{field}[{index}] values must be non-empty strings")
            continue
        items.append({key: item[key].strip() for key in required})
    return tuple(items)


def _load_spec(path: Path) -> PacketSpec:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PacketValidationError(path, [str(error)]) from error
    errors: list[str] = []
    if not isinstance(payload, dict):
        raise PacketValidationError(path, ["JSON root must be an object"])
    missing = sorted(REQUIRED_KEYS - set(payload))
    unknown = sorted(set(payload) - REQUIRED_KEYS)
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")

    if payload.get("version") != 1:
        errors.append("version must be 1")
    packet_id = payload.get("packet_id")
    if not isinstance(packet_id, str) or not PACKET_ID_RE.fullmatch(packet_id):
        errors.append("packet_id must be a safe lowercase slug")
        packet_id = "invalid"
    title = payload.get("title")
    if not isinstance(title, str) or not title.strip() or not HANGUL_RE.search(title):
        errors.append("title must be a non-empty Korean review title")
        title = ""
    repository_url = payload.get("repository_url")
    if not isinstance(repository_url, str) or not GITHUB_REPOSITORY_RE.fullmatch(
        repository_url
    ):
        errors.append("repository_url must be an https://github.com/owner/repo URL")
        repository_url = ""
    source_commit = payload.get("source_commit")
    if not isinstance(source_commit, str) or not source_commit.strip():
        errors.append("source_commit must be a Git ref or commit")
        source_commit = ""
    scope = payload.get("scope")
    if not isinstance(scope, str) or not scope.strip() or not HANGUL_RE.search(scope):
        errors.append("scope must be a non-empty Korean description")
        scope = ""

    source_payload = payload.get("sources")
    sources: list[SourceEntry] = []
    if not isinstance(source_payload, list) or not source_payload:
        errors.append("sources must be a non-empty object array")
    else:
        for index, item in enumerate(source_payload):
            if not isinstance(item, dict) or set(item) != {
                "path",
                "category",
                "description",
            }:
                errors.append(
                    f"sources[{index}] must contain exactly path, category, description"
                )
                continue
            source_path = _safe_relative_path(
                item.get("path"), field=f"sources[{index}].path", errors=errors
            )
            category = item.get("category")
            description = item.get("description")
            if category not in ALLOWED_CATEGORIES:
                errors.append(f"sources[{index}].category is not allowed")
                category = "context"
            if not isinstance(description, str) or not description.strip():
                errors.append(f"sources[{index}].description must be non-empty")
                description = ""
            sources.append(SourceEntry(source_path, category, description.strip()))
    paths = [source.path for source in sources]
    if len(paths) != len(set(paths)):
        errors.append("sources must not contain duplicate paths")

    references = _object_list(
        payload.get("references"),
        "references",
        frozenset({"label", "url"}),
        errors,
    )
    for index, reference in enumerate(references):
        if not reference["url"].startswith("https://"):
            errors.append(f"references[{index}].url must use https")
    exclusions = _object_list(
        payload.get("exclusions"),
        "exclusions",
        frozenset({"item", "reason"}),
        errors,
    )
    review_questions = _string_list(
        payload.get("review_questions"), "review_questions", errors
    )
    known_gaps = _string_list(payload.get("known_gaps"), "known_gaps", errors)

    narrative = "\n".join(
        [
            title,
            scope,
            *review_questions,
            *known_gaps,
            *(value for item in references for value in item.values()),
            *(value for item in exclusions for value in item.values()),
            *(source.description for source in sources),
        ]
    )
    errors.extend(f"spec {risk}" for risk in find_publication_risks(narrative))
    if errors:
        raise PacketValidationError(path, errors)

    canonical = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    return PacketSpec(
        packet_id=packet_id,
        title=title.strip(),
        repository_url=repository_url.rstrip("/"),
        source_commit=source_commit.strip(),
        scope=scope.strip(),
        sources=tuple(sources),
        references=references,
        review_questions=review_questions,
        known_gaps=known_gaps,
        exclusions=exclusions,
        canonical_json=canonical,
    )


def _decode_public_text(content: bytes, source_path: str) -> str:
    if b"\x00" in content:
        raise PacketValidationError(source_path, ["binary files are not supported in v1"])
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PacketValidationError(
            source_path, ["source is not valid UTF-8 text"]
        ) from error
    risks = find_publication_risks(text)
    if risks:
        raise PacketValidationError(
            source_path, [f"source {risk}" for risk in risks]
        )
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _render_readme(spec: PacketSpec, commit: str) -> str:
    source_rows = "\n".join(
        f"{index}. `{source.path}` — {source.category}: {source.description}"
        for index, source in enumerate(spec.sources, start=1)
    )
    references = "\n".join(
        f"- [{item['label']}]({item['url']})" for item in spec.references
    )
    questions = "\n".join(f"- {item}" for item in spec.review_questions)
    gaps = "\n".join(f"- {item}" for item in spec.known_gaps)
    exclusions = "\n".join(
        f"- **{item['item']}**: {item['reason']}" for item in spec.exclusions
    )
    return f"""# {spec.title}

## 평가 범위

{spec.scope}

- Source repository: {spec.repository_url}
- Immutable source commit: [`{commit}`]({spec.repository_url}/commit/{commit})
- Packet ID: `{spec.packet_id}`

## 읽는 순서

1. `REVIEW_PROMPT.md`
2. `PACKET_SPEC.json`
3. 아래 source snapshot
4. `MANIFEST.json`의 checksum과 제외 항목

{source_rows}

## 외부 참조

{references}

## 검토 질문

{questions}

## 알려진 공백

{gaps}

## 의도적으로 제외한 항목

{exclusions}

이 packet은 명시적 allowlist에 포함된 UTF-8 text만 담는다. 제외는 누락으로 숨기지 않고 위 목록과 manifest에 사유를 남긴다.
"""


def _render_review_prompt(spec: PacketSpec, commit: str) -> str:
    questions = "\n".join(f"- {question}" for question in spec.review_questions)
    return f"""# External AI Critical Review Prompt

당신은 `{spec.packet_id}`를 독립적으로 검토하는 비판적 reviewer다. 평가 대상 commit은 `{commit}`이다.

## 검토 원칙

- 작성자의 자기주장을 근거 없이 인정하지 않는다.
- 사실, 추론, 미확인을 분리한다.
- finding마다 packet 내부 file path와 가능한 경우 line 또는 section을 인용한다.
- correctness, scope fidelity, reproducibility, evidence sufficiency, privacy, leakage와 overengineering을 점검한다.
- test가 실제 failure mode를 재현하는지 확인한다.
- 공개되지 않았거나 packet에 없는 정보는 추측하지 않고 `unknown`으로 표시한다.
- private chain-of-thought를 요구하지 않는다. 공개된 결정 근거와 artifact만 평가한다.

## 프로젝트별 질문

{questions}

## 출력 형식

각 finding을 다음 형식으로 작성한다.

```text
Finding ID:
Severity: Critical | High | Medium | Low | Note
Status: Verified | Inferred | Unknown
Claim:
Evidence:
Impact:
Recommended action:
```

마지막에는 `검증된 강점`, `근거가 부족한 주장`, `가장 먼저 수정할 3개 항목`을 별도 section으로 정리한다.
"""


def _manifest_for(
    spec: PacketSpec, commit: str, files: Sequence[PlannedFile]
) -> Mapping[str, Any]:
    return {
        "schema_version": 1,
        "packet_id": spec.packet_id,
        "title": spec.title,
        "repository_url": spec.repository_url,
        "source_commit": commit,
        "spec_sha256": hashlib.sha256(spec.canonical_json).hexdigest(),
        "files": [
            {
                "path": file.path,
                "category": file.category,
                "source_path": file.source_path,
                "description": file.description,
                "bytes": len(file.content),
                "sha256": file.sha256,
            }
            for file in sorted(files, key=lambda item: item.path)
        ],
        "references": list(spec.references),
        "known_gaps": list(spec.known_gaps),
        "exclusions": list(spec.exclusions),
    }


def build_packet_plan(
    spec_path: Path, source_reader: SourceReader
) -> PacketPlan:
    """Validate a spec and return the entire packet in memory."""

    spec = _load_spec(Path(spec_path))
    try:
        commit = source_reader.resolve_commit(spec.source_commit)
    except RuntimeError as error:
        raise PacketValidationError(spec_path, [f"cannot resolve source commit: {error}"]) from error

    files: list[PlannedFile] = []
    for source in spec.sources:
        try:
            raw = source_reader.read_file(commit, source.path)
        except RuntimeError as error:
            raise PacketValidationError(
                spec_path, [f"cannot read {source.path} at {commit}: {error}"]
            ) from error
        normalized = _decode_public_text(raw, source.path).encode("utf-8")
        files.append(
            PlannedFile(
                path=f"sources/{source.path}",
                content=normalized,
                category=source.category,
                source_path=source.path,
                description=source.description,
            )
        )

    generated = (
        PlannedFile(
            "README.md",
            _render_readme(spec, commit).encode("utf-8"),
            "index",
        ),
        PlannedFile(
            "REVIEW_PROMPT.md",
            _render_review_prompt(spec, commit).encode("utf-8"),
            "review_prompt",
        ),
        PlannedFile("PACKET_SPEC.json", spec.canonical_json, "packet_spec"),
    )
    for file in generated:
        risks = find_publication_risks(file.content.decode("utf-8"))
        if risks:
            raise PacketValidationError(
                spec_path, [f"generated {file.path} {risk}" for risk in risks]
            )
    all_files = tuple([*generated, *files])
    manifest = _manifest_for(spec, commit, all_files)
    return PacketPlan(
        packet_id=spec.packet_id,
        title=spec.title,
        repository_url=spec.repository_url,
        source_commit=commit,
        files=all_files,
        manifest=manifest,
    )


def render_plan(plan: PacketPlan) -> str:
    """Render a compact, read-only build preview."""

    lines = [
        f"Packet: {plan.packet_id}",
        f"Title: {plan.title}",
        f"Source commit: {plan.source_commit}",
        f"Files: {len(plan.files) + 1} including MANIFEST.json",
    ]
    lines.extend(
        f"- {file.path} ({len(file.content)} bytes, sha256={file.sha256[:12]}...)"
        for file in sorted(plan.files, key=lambda item: item.path)
    )
    return "\n".join(lines) + "\n"


def _target_path(root: Path, packet_id: str) -> Path:
    resolved_root = root.resolve()
    target = (resolved_root / packet_id).resolve()
    if target.parent != resolved_root:
        raise PacketValidationError(root, ["packet target escaped output root"])
    return target


def write_packet(plan: PacketPlan, output_root: Path) -> Path:
    """Atomically write one new packet; existing packets are immutable."""

    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = _target_path(root, plan.packet_id)
    if target.exists():
        raise FileExistsError(f"packet already exists and is immutable: {target}")

    temp = Path(tempfile.mkdtemp(prefix=f".{plan.packet_id}-", dir=root))
    try:
        for file in plan.files:
            destination = temp / PurePosixPath(file.path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(file.content)
        manifest_text = json.dumps(
            plan.manifest, ensure_ascii=False, sort_keys=True, indent=2
        ) + "\n"
        (temp / "MANIFEST.json").write_text(manifest_text, encoding="utf-8")
        verify_packet(temp, expected_packet_id=plan.packet_id)
        temp.rename(target)
    except Exception:
        if temp.exists() and temp.parent == root and temp.name.startswith(
            f".{plan.packet_id}-"
        ):
            shutil.rmtree(temp)
        raise
    return target


def verify_packet(
    packet_dir: Path, *, expected_packet_id: str | None = None
) -> Mapping[str, Any]:
    """Verify manifest completeness, file sizes, and SHA256 hashes."""

    root = Path(packet_dir).resolve()
    manifest_path = root / "MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PacketValidationError(root, [f"cannot read MANIFEST.json: {error}"]) from error
    errors: list[str] = []
    packet_id = manifest.get("packet_id")
    if expected_packet_id is not None and packet_id != expected_packet_id:
        errors.append("manifest packet_id does not match the build plan")
    if root.name != packet_id and expected_packet_id is None:
        errors.append("directory name does not match manifest packet_id")
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise PacketValidationError(root, ["manifest files must be an array"])

    expected_paths: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not all(
            key in entry for key in ("path", "bytes", "sha256")
        ):
            errors.append(f"manifest files[{index}] is invalid")
            continue
        path_value = entry["path"]
        safe_path = _safe_relative_path(
            path_value, field=f"manifest files[{index}].path", errors=errors
        )
        if not safe_path:
            continue
        expected_paths.add(safe_path)
        file_path = (root / PurePosixPath(safe_path)).resolve()
        if root not in file_path.parents:
            errors.append(f"manifest path escaped packet root: {safe_path}")
            continue
        if not file_path.is_file():
            errors.append(f"manifest file is missing: {safe_path}")
            continue
        content = file_path.read_bytes()
        if len(content) != entry["bytes"]:
            errors.append(f"size mismatch: {safe_path}")
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            errors.append(f"sha256 mismatch: {safe_path}")

    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "MANIFEST.json"
    }
    extra = sorted(actual_paths - expected_paths)
    missing = sorted(expected_paths - actual_paths)
    if extra:
        errors.append(f"untracked packet files: {', '.join(extra)}")
    if missing:
        errors.append(f"missing packet files: {', '.join(missing)}")
    if errors:
        raise PacketValidationError(root, errors)
    return manifest
