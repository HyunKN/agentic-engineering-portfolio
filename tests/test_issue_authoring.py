from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.issue_authoring import (
    DraftValidationError,
    GithubPublisher,
    prepare_drafts,
    render_preview,
)


def valid_work_draft() -> dict[str, object]:
    return {
        "version": 1,
        "repository": "HyunKN/agentic-engineering-portfolio",
        "issue_number": 10,
        "parent_issue": 4,
        "kind": "work",
        "title": "[M0-005][FND-012] AI Issue 작성·검증 Workflow 구축",
        "body": (
            "## 목표\r\n\r\n안전한 Issue 작성 workflow를 만든다.\r\n\r\n"
            "## 작업 범위\r\n\r\n- JSON draft 검증\r\n\r\n"
            "## 완료 기준\r\n\r\n- [ ] 줄바꿈을 보존한다.  \r\n\r\n"
            "## 검증 계획\r\n\r\nunit test로 확인한다.\r\n"
        ),
        "labels": [
            "track:foundation",
            "type:implementation",
            "priority:p0",
        ],
        "milestone": "M0 - Foundation and task system",
    }


class DraftTestCase(unittest.TestCase):
    def prepare(self, payload: object):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "draft.json"
            path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            return prepare_drafts([path])

    def test_valid_draft_normalizes_crlf_and_trailing_whitespace(self) -> None:
        draft = self.prepare(valid_work_draft())[0]

        self.assertNotIn("\r", draft.body)
        self.assertIn("- [ ] 줄바꿈을 보존한다.\n", draft.body)
        self.assertTrue(draft.body.endswith("\n"))

    def test_preview_is_read_only_and_contains_rendered_body(self) -> None:
        draft = self.prepare(valid_work_draft())[0]

        preview = render_preview([draft])

        self.assertIn("=== UPDATE", preview)
        self.assertIn(draft.title, preview)
        self.assertIn("## 완료 기준", preview)

    def test_rejects_inline_checklist_caused_by_newline_collapse(self) -> None:
        payload = valid_work_draft()
        payload["body"] = str(payload["body"]).replace(
            "\r\n\r\n- [ ] 줄바꿈", " - [ ] 줄바꿈"
        )

        with self.assertRaisesRegex(
            DraftValidationError, "possible newline collapse"
        ):
            self.prepare(payload)

    def test_rejects_missing_required_heading(self) -> None:
        payload = valid_work_draft()
        payload["body"] = str(payload["body"]).replace("## 검증 계획", "검증")

        with self.assertRaisesRegex(DraftValidationError, "## 검증 계획"):
            self.prepare(payload)

    def test_rejects_invalid_execution_order(self) -> None:
        payload = valid_work_draft()
        payload["title"] = "[M0-011][FND-012] 잘못된 실행 순서"

        with self.assertRaisesRegex(DraftValidationError, "positive 5-step"):
            self.prepare(payload)

    def test_rejects_unknown_or_duplicated_label_axes(self) -> None:
        payload = valid_work_draft()
        payload["labels"] = [
            "track:foundation",
            "track:portfolio",
            "type:implementation",
            "priority:p0",
            "unknown:label",
        ]

        with self.assertRaises(DraftValidationError) as raised:
            self.prepare(payload)

        message = str(raised.exception)
        self.assertIn("unknown labels", message)
        self.assertIn("exactly one track:", message)

    def test_rejects_local_machine_path(self) -> None:
        payload = valid_work_draft()
        payload["body"] = str(payload["body"]).replace(
            "안전한 Issue", r"C:\Users\hi\secret에서 Issue"
        )

        with self.assertRaisesRegex(DraftValidationError, "local machine path"):
            self.prepare(payload)

    def test_rejects_secret_pattern_in_title(self) -> None:
        payload = valid_work_draft()
        payload["title"] = (
            "[M0-005][FND-012] 위험한 토큰 " + "ghp_" + "a" * 24
        )

        with self.assertRaisesRegex(DraftValidationError, "secret pattern"):
            self.prepare(payload)


class FakeRunner:
    def __init__(self, remote: dict[str, object]) -> None:
        self.remote = remote
        self.calls: list[tuple[list[str], str | None]] = []

    def __call__(self, args, *, input, text, capture_output, check):
        self.calls.append((list(args), input))
        if args[1:3] == ["issue", "view"]:
            output = json.dumps(self.remote, ensure_ascii=False)
        else:
            output = ""
        return subprocess.CompletedProcess(args, 0, output, "")


class PublisherTestCase(unittest.TestCase):
    def prepare(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "draft.json"
            path.write_text(
                json.dumps(valid_work_draft(), ensure_ascii=False), encoding="utf-8"
            )
            return prepare_drafts([path])[0]

    def test_publisher_uses_stdin_body_file_and_verifies_round_trip(self) -> None:
        draft = self.prepare()
        runner = FakeRunner(
            {
                "title": draft.title,
                "body": draft.body,
                "milestone": {"title": draft.milestone},
                "labels": [{"name": label} for label in draft.labels],
            }
        )

        url = GithubPublisher(runner=runner).publish(draft)

        self.assertEqual(
            "https://github.com/HyunKN/agentic-engineering-portfolio/issues/10",
            url,
        )
        edit_args, edit_body = runner.calls[0]
        self.assertIn("--body-file", edit_args)
        self.assertIn("-", edit_args)
        self.assertNotIn("--body", edit_args)
        self.assertEqual(draft.body, edit_body)
        self.assertEqual(["gh", "issue", "edit"], runner.calls[1][0][:3])
        self.assertIn("--parent", runner.calls[1][0])


if __name__ == "__main__":
    unittest.main()
