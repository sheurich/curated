import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402


class TestCuratedSite(unittest.TestCase):
    def test_data_validates_cleanly(self) -> None:
        data = json.loads(build.DATA_PATH.read_text(encoding="utf-8"))
        errors = build.validate_payload(data)
        self.assertEqual(errors, [])

    def test_initial_entry_present(self) -> None:
        data = json.loads(build.DATA_PATH.read_text(encoding="utf-8"))
        urls = {r["url"]: r for r in data["resources"]}
        self.assertIn("https://lastmuseum.com/", urls)
        entry = urls["https://lastmuseum.com/"]
        for expected_tag in ("art", "museum", "free"):
            self.assertIn(expected_tag, entry["tags"])

    def test_build_outputs_exist_and_contain_features(self) -> None:
        rc = build.build()
        self.assertEqual(rc, 0)

        index_html = (build.SITE_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://lastmuseum.com/", index_html)
        self.assertIn("The Last Museum", index_html)
        self.assertIn('data-theme="auto"', index_html)
        self.assertIn("prefers-color-scheme: dark", index_html)
        self.assertIn('data-view="cards"', index_html)
        self.assertIn('data-view="index"', index_html)
        self.assertIn('data-view="directory"', index_html)
        self.assertIn('data-view="tags"', index_html)

        bookmarks = (build.SITE_DIR / "bookmarks.html").read_text(encoding="utf-8")
        self.assertIn("NETSCAPE-Bookmark-file-1", bookmarks)
        self.assertIn("https://lastmuseum.com/", bookmarks)

        readme = build.README_PATH.read_text(encoding="utf-8")
        self.assertIn("https://lastmuseum.com/", readme)
        self.assertIn("`#art`", readme)
        self.assertIn("`#museum`", readme)
        self.assertIn("`#free`", readme)

    def test_security_validation_rejects_dangerous_schemes_and_control_chars(self) -> None:
        base = json.loads(build.DATA_PATH.read_text(encoding="utf-8"))
        bad = json.loads(json.dumps(base))
        bad["resources"].append(
            {
                "id": "bad-entry",
                "title": "Bad \x1b[31mEntry",
                "url": "javascript:alert(1)",
                "category": "arts-culture",
                "scopes": ["family"],
                "tags": ["art"],
                "added": "2026-10-22",
            }
        )
        errors = build.validate_payload(bad)
        self.assertTrue(any("invalid http(s) url" in e for e in errors))
        self.assertTrue(any("disallowed control characters" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
