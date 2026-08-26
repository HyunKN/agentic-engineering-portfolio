from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from agent_workflows.evaluation_packet import (
    PacketValidationError,
    build_packet_plan,
    render_plan,
    verify_packet,
    write_packet,
)


COMMIT = "a" * 40


class InMemorySourceReader:
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    def resolve_commit(self, ref: str) -> str:
        if ref != "main":
            raise RuntimeError(f"unknown ref: {ref}")
        return COMMIT

    def read_file(self, commit: str, path: str) -> bytes:
        if commit != COMMIT or path not in self.files:
            raise RuntimeError(f"unknown blob: {commit}:{path}")
        return self.files[path]


def valid_spec() -> dict[str, object]:
    return {
        "version": 1,
        "packet_id": "workflow-review-v1",
        "title": "Workflow 공개 검토 자료",
        "repository_url": "https://github.com/HyunKN/agentic-engineering-portfolio",
        "source_commit": "main",
        "scope": "두 workflow의 경계와 공개 검증 가능성을 평가한다.",
        "sources": [
            {
                "path": "docs/design.md",
                "category": "decision",
                "description": "설계 결정과 module boundary",
            },
            {
                "path": "tests/test_workflow.py",
                "category": "test",
                "description": "주요 실패 조건 regression test",
            },
        ],
        "references": [
            {
                "label": "구현 Issue",
                "url": "https://github.com/HyunKN/agentic-engineering-portfolio/issues/11",
            }
        ],
        "review_questions": [
            "module 경계가 과도한 추상화 없이 독립적인가?",
            "검증 근거가 주장에 충분한가?",
        ],
        "known_gaps": ["외부 Web AI 호출과 review 저장은 아직 수동이다."],
        "exclusions": [
            {
                "item": "비공개 대화 원문",
                "reason": "개인정보와 숨겨진 지시가 섞일 수 있어 공개하지 않는다.",
            }
        ],
    }


class EvaluationPacketTestCase(unittest.TestCase):
    def write_spec(self, directory: str, payload: object) -> Path:
        path = Path(directory) / "packet.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
        return path

    def reader(self, *, design: bytes = b"design\r\n") -> InMemorySourceReader:
        return InMemorySourceReader(
            {
                "docs/design.md": design,
                "tests/test_workflow.py": b"def test_workflow():\n    assert True\n",
            }
        )

    def test_plan_uses_resolved_commit_and_normalizes_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plan = build_packet_plan(
                self.write_spec(temp_dir, valid_spec()), self.reader()
            )

        self.assertEqual(COMMIT, plan.source_commit)
        files = {file.path: file for file in plan.files}
        self.assertEqual(b"design\n", files["sources/docs/design.md"].content)
        self.assertIn(COMMIT, files["README.md"].content.decode("utf-8"))
        manifest_entry = next(
            item
            for item in plan.manifest["files"]
            if item["path"] == "sources/docs/design.md"
        )
        self.assertEqual(
            hashlib.sha256(b"design\n").hexdigest(), manifest_entry["sha256"]
        )

    def test_preview_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = build_packet_plan(self.write_spec(temp_dir, valid_spec()), self.reader())

            preview = render_plan(plan)

            self.assertIn("Packet: workflow-review-v1", preview)
            self.assertFalse((root / "workflow-review-v1").exists())

    def test_rejects_parent_path_traversal(self) -> None:
        payload = valid_spec()
        payload["sources"][0]["path"] = "../private.txt"
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(PacketValidationError, "traverse parents"):
                build_packet_plan(self.write_spec(temp_dir, payload), self.reader())

    def test_rejects_secret_or_local_path_in_source(self) -> None:
        secret = "ghp_" + "a" * 24
        local_path = "C:" + r"\Users\hi\private"
        unsafe = f"token={secret}\npath={local_path}\n".encode("utf-8")
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(PacketValidationError) as raised:
                build_packet_plan(
                    self.write_spec(temp_dir, valid_spec()),
                    self.reader(design=unsafe),
                )

        message = str(raised.exception)
        self.assertIn("secret pattern", message)
        self.assertIn("local machine path", message)
        self.assertNotIn(secret, message)
        self.assertNotIn(local_path, message)

    def test_write_verify_tamper_and_immutable_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = build_packet_plan(self.write_spec(temp_dir, valid_spec()), self.reader())

            packet = write_packet(plan, root / "packets")
            manifest = verify_packet(packet)

            self.assertEqual(COMMIT, manifest["source_commit"])
            with self.assertRaisesRegex(FileExistsError, "immutable"):
                write_packet(plan, root / "packets")

            (packet / "README.md").write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(PacketValidationError, "mismatch"):
                verify_packet(packet)

    def test_verify_rejects_untracked_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = build_packet_plan(self.write_spec(temp_dir, valid_spec()), self.reader())
            packet = write_packet(plan, root / "packets")
            (packet / "untracked.txt").write_text("extra\n", encoding="utf-8")

            with self.assertRaisesRegex(PacketValidationError, "untracked"):
                verify_packet(packet)


if __name__ == "__main__":
    unittest.main()
