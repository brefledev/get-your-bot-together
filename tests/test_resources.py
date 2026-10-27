import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "resources", Path(__file__).resolve().parents[1] / "tools/check_resources.py"
)
resources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resources)


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_valid_resources_and_fenced_examples(self):
        self.write("README.md", "# Start\n[Page](page.md#use-it)\n"
                   "```md\n[Example](missing.md)\n```\n")
        self.write("page.md", "# Use it\n[Back](README.md)\n")
        self.write("data.json", '{"ok":true}')
        self.write("config.toml", 'name = "example"')
        result = resources.check(self.root)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["checked"]["links"], 2)

    def test_missing_link_and_heading(self):
        self.write("README.md", "[Missing](missing.md)\n[Heading](page.md#missing)")
        self.write("page.md", "# Present")
        errors = resources.check(self.root)["errors"]
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("missing target" in e for e in errors))
        self.assertTrue(any("missing heading" in e for e in errors))

    def test_picture_sources_and_fallback(self):
        self.write("README.md", '<picture><source srcset="narrow.png 1x, missing.png 2x">'
                   '<img src="wide.png" alt="Workflow"></picture>')
        self.write("narrow.png", "fixture")
        self.write("wide.png", "fixture")
        result = resources.check(self.root)
        self.assertFalse(result["passed"])
        self.assertEqual(result["checked"]["links"], 3)
        self.assertEqual(result["errors"], ["README.md: missing target: missing.png"])

    def test_escape_and_absolute_paths(self):
        self.write("README.md", "[Escape](../outside.md)\n[Local](/etc/passwd)")
        errors = resources.check(self.root)["errors"]
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("leaves repository" in e for e in errors))

    def test_invalid_config(self):
        self.write("data.json", "{broken")
        self.write("config.toml", "name =")
        self.assertEqual(len(resources.check(self.root)["errors"]), 2)

    def test_private_path(self):
        self.write("README.md", "Copied from C:/Users/example/private.md")
        self.assertFalse(resources.check(self.root)["passed"])

    def test_role_fields(self):
        self.write("setup/codex/source.toml", 'name = "source"')
        self.write("setup/cursor/reviewer.md", "# No frontmatter")
        result = resources.check(self.root)
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["errors"]), 3)

    def test_encoded_names_and_duplicate_headings(self):
        self.write("README.md", "[Page](My%20Page.md#same-1)")
        self.write("My Page.md", "# Same\n# Same\n")
        self.assertTrue(resources.check(self.root)["passed"])


if __name__ == "__main__":
    unittest.main()
