import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import kitty_chronicles_generator as generator


PASSAGE = {
    "id": "test-passage",
    "reference": "Test 1:1–9",
    "summary": "A faithful family listens carefully, helps a neighbor, and learns to trust God together.",
}


def write_ledger(root: Path, used=None, candidates=None):
    path = root / generator.LEDGER_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "used": used or [],
                "candidates": candidates if candidates is not None else [PASSAGE],
            }
        ),
        encoding="utf-8",
    )


class KittyChroniclesTests(unittest.TestCase):
    def test_used_passage_cannot_be_selected(self):
        ledger = {"used": [PASSAGE], "candidates": []}
        with self.assertRaises(generator.ValidationError):
            generator.select_passage(ledger, "test-passage")

    def test_story_validator_requires_every_recurring_character(self):
        payload = generator.dry_payload(PASSAGE)
        payload["body"] = payload["body"].replace("Tumbles", "the kitten")
        with self.assertRaisesRegex(generator.ValidationError, "Tumbles"):
            generator.validate_story(payload, PASSAGE, set())

    def test_dry_run_writes_valid_story_image_and_updated_ledger(self):
        with tempfile.TemporaryDirectory() as source_name, tempfile.TemporaryDirectory() as output_name:
            source = Path(source_name)
            output = Path(output_name)
            (source / generator.STORY_DIR).mkdir()
            write_ledger(source)
            result = generator.generate(source, output, "dry-run", None, output / "metadata.json")

            self.assertTrue((output / result["story_file"]).exists())
            self.assertTrue((output / result["image_file"]).exists())
            self.assertTrue((output / "metadata.json").exists())
            with Image.open(output / result["image_file"]) as image:
                self.assertEqual(image.size, generator.IMAGE_SIZE)
                self.assertEqual(image.format, "PNG")
            updated = json.loads((output / generator.LEDGER_PATH).read_text(encoding="utf-8"))
            self.assertEqual(updated["candidates"], [])
            self.assertEqual(updated["used"][0]["reference"], PASSAGE["reference"])

    def test_repository_validator_rejects_duplicate_scripture(self):
        with tempfile.TemporaryDirectory() as root_name:
            root = Path(root_name)
            story_dir = root / generator.STORY_DIR
            image_dir = root / generator.IMAGE_DIR
            story_dir.mkdir(parents=True)
            image_dir.mkdir(parents=True)
            image_path = image_dir / "one.png"
            generator.placeholder_image(image_path)
            front = """---
layout: post
title: "One"
date: 2026-01-01 08:00:00 -05:00
image: /ezra-blog/assets/images/family/kittychronicles/volume-2/one.png
excerpt: "A sufficiently descriptive excerpt for a repository validation fixture and duplicate passage test."
volume: 2
order: 1
scripture: "Test 1:1–9"
published: true
---

Body.
"""
            (story_dir / "one.md").write_text(front, encoding="utf-8")
            (story_dir / "two.md").write_text(front.replace('title: "One"', 'title: "Two"'), encoding="utf-8")
            write_ledger(
                root,
                used=[
                    {
                        "id": PASSAGE["id"],
                        "reference": PASSAGE["reference"],
                        "story_file": "_kittychronicles/one.md",
                        "image_file": "assets/images/family/kittychronicles/volume-2/one.png",
                    }
                ],
                candidates=[],
            )
            with self.assertRaisesRegex(generator.ValidationError, "Duplicate scripture"):
                generator.validate_repository(root)


if __name__ == "__main__":
    unittest.main()
