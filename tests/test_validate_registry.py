import json
import unittest
from pathlib import Path

from scripts.validate_registry import validate_registry

ROOT = Path(__file__).resolve().parents[1]
SHA = "0000000000000000000000000000000000000000"


class RegistryValidationTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "config/sources.example.json").read_text(encoding="utf-8"))

    def test_example_is_valid(self):
        validate_registry(self.registry)

    def test_rejects_plain_http(self):
        self.registry["sources"][0]["url"] = f"http://raw.githubusercontent.com/example/repo/{SHA}/file.json"
        with self.assertRaisesRegex(ValueError, "must be HTTPS"):
            validate_registry(self.registry)

    def test_rejects_duplicate_ids(self):
        self.registry["sources"].append(dict(self.registry["sources"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate identifier"):
            validate_registry(self.registry)

    def test_rejects_url_credentials(self):
        self.registry["sources"][0]["url"] = f"https://user:secret@raw.githubusercontent.com/example/repo/{SHA}/file.json"
        with self.assertRaisesRegex(ValueError, "without embedded credentials"):
            validate_registry(self.registry)

    def test_rejects_moving_github_revision(self):
        self.registry["sources"][0]["url"] = "https://raw.githubusercontent.com/example-owner/example-repo/main/sing-box.json"
        with self.assertRaisesRegex(ValueError, "URL path must contain"):
            validate_registry(self.registry)

    def test_rejects_oversized_limits(self):
        self.registry["sources"][0]["maxBytes"] = 1048577
        with self.assertRaisesRegex(ValueError, "maxBytes"):
            validate_registry(self.registry)

    def test_rejects_malformed_url(self):
        self.registry["sources"][0]["url"] = "https://[broken"
        with self.assertRaisesRegex(ValueError, "must be HTTPS"):
            validate_registry(self.registry)

    def test_rejects_private_ip_endpoint(self):
        self.registry["sources"][0]["kind"] = "subscription"
        self.registry["sources"][0]["format"] = "share-links"
        self.registry["sources"][0].pop("revision")
        self.registry["sources"][0]["url"] = "https://127.0.0.1/feed"
        with self.assertRaisesRegex(ValueError, "non-public IP"):
            validate_registry(self.registry)

    def test_rejects_wrong_type_for_kind(self):
        self.registry["sources"][0]["kind"] = []
        with self.assertRaisesRegex(ValueError, "unsupported source kind"):
            validate_registry(self.registry)

    def test_rejects_boolean_schema_version(self):
        self.registry["schemaVersion"] = True
        with self.assertRaisesRegex(ValueError, "schemaVersion"):
            validate_registry(self.registry)


if __name__ == "__main__":
    unittest.main()
