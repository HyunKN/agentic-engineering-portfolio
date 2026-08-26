from __future__ import annotations

from pathlib import Path
import unittest

from agent_workflows.publication_safety import find_publication_risks


class PublicationSafetyTestCase(unittest.TestCase):
    def test_detects_supported_local_path_forms(self) -> None:
        windows_path = "C:" + r"\Users\example\private.txt"
        slash_path = "/" + "C:/Users/example/private.txt"

        self.assertIn(
            "contains a local machine path", find_publication_risks(windows_path)
        )
        self.assertIn(
            "contains a local machine path", find_publication_risks(slash_path)
        )

    def test_detector_source_does_not_flag_itself(self) -> None:
        source = (
            Path(__file__).parents[1] / "agent_workflows" / "publication_safety.py"
        ).read_text(encoding="utf-8")

        self.assertEqual((), find_publication_risks(source))


if __name__ == "__main__":
    unittest.main()
