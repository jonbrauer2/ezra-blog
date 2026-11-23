#!/usr/bin/env python3
"""Generate, validate, and stage one Kitty Chronicles Volume 2 story."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = Path("_data/kitty_chronicles_passages.json")
STORY_DIR = Path("_kittychronicles")
IMAGE_DIR = Path("assets/images/family/kittychronicles/volume-2")
REQUIRED_CHARACTERS = ("Hadley", "Grayson", "Colton", "Tumbles")
MIN_WORDS = 1200
MAX_WORDS = 2800
IMAGE_SIZE = (1536, 1024)


class ValidationError(RuntimeError):
    pass


def canonical(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value[:72] or "kitty-chronicle"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_ledger(root: Path) -> dict[str, Any]:
    path = root / LEDGER_PATH
    if not path.exists():
        raise ValidationError(f"Missing passage ledger: {path}")
    data = load_json(path)
    if data.get("schema_version") != 1:
        raise ValidationError("Passage ledger schema_version must be 1")
    used = data.get("used", [])
    candidates = data.get("candidates", [])
    ids = [item.get("id") for item in used + candidates]
    refs = [canonical(item.get("reference", "")) for item in used + candidates]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValidationError("Passage IDs must be present and unique")
    if any(not item for item in refs) or len(refs) != len(set(refs)):
        raise ValidationError("Passage references must be present and unique")
    for item in candidates:
        if len(item.get("summary", "").split()) < 8:
            raise ValidationError(f"Candidate {item['id']} needs a factual summary")
    return data


def select_passage(ledger: dict[str, Any], requested: str | None = None) -> dict[str, str]:
    candidates = ledger["candidates"]
    if requested:
        match = next((item for item in candidates if item["id"] == requested), None)
        if not match:
            raise ValidationError(f"Unknown or already-used passage_id: {requested}")
        return match
    if not candidates:
        raise ValidationError("No unused passages remain in the catalog")
    return sorted(candidates, key=lambda item: item["id"])[0]


def parse_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        if value.casefold() in {"true", "false"}:
            result[key.strip()] = value.casefold() == "true"
        elif value.isdigit():
            result[key.strip()] = int(value)
        else:
            result[key.strip()] = value
    return result


def existing_titles(root: Path) -> set[str]:
    return {canonical(parse_front_matter(path).get("title", "")) for path in (root / STORY_DIR).glob("*.md")}


def next_order(root: Path) -> int:
    orders = [
        int(meta.get("order", 0))
        for path in (root / STORY_DIR).glob("*.md")
        if (meta := parse_front_matter(path)).get("volume") == 2
    ]
    return max(orders, default=0) + 1


def validate_story(payload: dict[str, Any], passage: dict[str, str], titles: set[str]) -> None:
    required = {"title", "excerpt", "body", "image_scene"}
    if set(payload) != required:
        raise ValidationError(f"Story JSON must contain exactly: {sorted(required)}")
    title = payload["title"].strip()
    excerpt = payload["excerpt"].strip()
    body = payload["body"].strip()
    scene = payload["image_scene"].strip()
    if not 8 <= len(title) <= 100 or canonical(title) in titles:
        raise ValidationError("Title is invalid or duplicates an existing story")
    if not 80 <= len(excerpt) <= 220:
        raise ValidationError("Excerpt must be 80-220 characters")
    count = len(re.findall(r"\b[\w’'-]+\b", body))
    if not MIN_WORDS <= count <= MAX_WORDS:
        raise ValidationError(f"Story must be {MIN_WORDS}-{MAX_WORDS} words; found {count}")
    missing = [name for name in REQUIRED_CHARACTERS if name not in body]
    if missing:
        raise ValidationError(f"Story is missing required characters: {', '.join(missing)}")
    if body.count("\n\n") < 18:
        raise ValidationError("Story needs at least 19 readable paragraphs")
    if re.search(r"<(?:script|iframe|audio)|\{\{|\{%|TODO|PLACEHOLDER", body, re.I):
        raise ValidationError("Story contains unsafe markup or placeholder text")
    ending = f"Based on {passage['reference']}."
    if not body.endswith(ending):
        raise ValidationError(f"Story must end exactly with: {ending}")
    if not 40 <= len(scene) <= 800:
        raise ValidationError("image_scene must be 40-800 characters")


def json_from_response(text: str) -> dict[str, Any]:
    text = text.strip()
    ticks = chr(96) * 3
    if text.startswith(ticks):
        text = text.removeprefix(ticks + "json").removeprefix(ticks).removesuffix(ticks).strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Model returned invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError("Model response must be a JSON object")
    return value


def client() -> Any:
    from openai import OpenAI

    kwargs = {"api_key": os.environ["OPENAI_API_KEY"]}
    if os.getenv("OPENAI_ORG_ID"):
        kwargs["organization"] = os.environ["OPENAI_ORG_ID"]
    if os.getenv("OPENAI_PROJECT_ID"):
        kwargs["project"] = os.environ["OPENAI_PROJECT_ID"]
    return OpenAI(**kwargs)


def writer_prompt(passage: dict[str, str], feedback: list[str]) -> str:
    return f"""Write one original Kitty Chronicles Volume 2 story as strict JSON.
Passage: {passage['reference']}
Factual Bible summary: {passage['summary']}
Required recurring characters: Hadley, Grayson, Colton, and Tumbles, one small orange tabby kitten.
Tone and format: warm, playful, cinematic bedtime adventure for ages 6-12; faithful to the supplied passage; 1,400-2,400 words; many short paragraphs; gentle humor; no headings, HTML, Markdown images, audio, or invented Bible quotations. The children may observe the biblical events as a story device, but must not replace biblical people or change the outcome. Include a thoughtful application without claiming that every prayer produces the same miracle. End exactly with "Based on {passage['reference']}."
Return only a JSON object with string keys title, excerpt, body, and image_scene. The excerpt is 80-220 characters. image_scene describes one visual climax without text or logos.
Revision feedback: {json.dumps(feedback)}"""


def reviewer_prompt(payload: dict[str, Any], passage: dict[str, str]) -> str:
    example = '{"approved": true, "issues": []}'
    return f"""Act as a strict children's Bible-story editor. Compare the draft with the supplied factual summary and reject any changed outcome, invented doctrine, unsafe content, missing recurring character, duplicate-feeling title, or format violation.
Passage: {passage['reference']}
Summary: {passage['summary']}
Draft: {json.dumps(payload, ensure_ascii=False)}
Return only JSON shaped like {example}."""


def generate_story(passage: dict[str, str], titles: set[str]) -> dict[str, Any]:
    api = client()
    model = os.getenv("KITTY_STORY_MODEL", "gpt-6.1-sol")
    feedback: list[str] = []
    for _ in range(3):
        response = api.responses.create(
            model=model,
            instructions="Return only valid JSON. Do not use Markdown fences.",
            input=writer_prompt(passage, feedback),
        )
        payload = json_from_response(response.output_text)
        try:
            validate_story(payload, passage, titles)
        except ValidationError as exc:
            feedback = [str(exc)]
            continue
        review = api.responses.create(
            model=model,
            instructions="Return only valid JSON. Do not use Markdown fences.",
            input=reviewer_prompt(payload, passage),
        )
        verdict = json_from_response(review.output_text)
        issues = verdict.get("issues", [])
        if verdict.get("approved") is True and issues == []:
            return payload
        feedback = [str(issue) for issue in issues] or ["Editorial review did not approve the draft"]
    raise ValidationError(f"Story failed generation/editorial review: {feedback}")


def dry_payload(passage: dict[str, str]) -> dict[str, str]:
    paragraphs = []
    for index in range(34):
        paragraphs.append(
            f"Hadley studied the path while Grayson checked the map and Colton whispered a brave plan to Tumbles. "
            f"The small orange kitten flicked his tail as lesson {index + 1} unfolded: {passage['summary']} "
            "Together they listened, asked careful questions, helped one another, and remembered that courage begins with trusting God."
        )
    paragraphs.append(
        "Uncle Jonathan reminded them that this adventure was not a magic formula, but a true account that showed God's character and invited faithful choices."
    )
    paragraphs.append(f"Based on {passage['reference']}.")
    return {
        "title": f"Tumbles and the Sunday Test: {passage['reference']}",
        "excerpt": "A deterministic test adventure proves the weekly generator, duplicate checks, illustration pipeline, and review-only publishing guard.",
        "body": "\n\n".join(paragraphs),
        "image_scene": "Hadley, Grayson, and Colton stand on a sunlit Bible-era path while Tumbles, a small orange tabby, watches from a stone.",
    }


def image_prompt(scene: str) -> str:
    return f"""Create a 3:2 landscape hero illustration matching an established cinematic, photorealistic children's Bible adventure series. Warm natural light, expressive faces, historically plausible Bible-era setting, family-friendly, no text, no logo, no border.
Recurring characters must be visually consistent: Hadley is a 10-year-old girl with wavy light-brown hair; Grayson is an 8-year-old boy with tousled light-brown hair; Colton is a 6-year-old boy; Tumbles is exactly one small orange tabby kitten. If Uncle Jonathan appears, he is early 40s with light-brown hair, black rectangular glasses, khaki clothes, and a backpack.
Scene: {scene}"""


def generate_image(path: Path, scene: str) -> None:
    response = client().images.generate(
        model=os.getenv("KITTY_IMAGE_MODEL", "gpt-image-2"),
        prompt=image_prompt(scene),
        size="1536x1024",
        quality=os.getenv("KITTY_IMAGE_QUALITY", "high"),
    )
    item = response.data[0]
    if getattr(item, "b64_json", None):
        data = base64.b64decode(item.b64_json)
    elif getattr(item, "url", None):
        with urllib.request.urlopen(item.url, timeout=90) as source:
            data = source.read()
    else:
        raise ValidationError("Image API returned neither b64_json nor URL")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def placeholder_image(path: Path) -> None:
    image = Image.new("RGB", IMAGE_SIZE, "#e8c98d")
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 60, 1476, 964), outline="#745331", width=8)
    draw.text((110, 110), "KITTY CHRONICLES DRY RUN", fill="#3b2918")
    draw.text((110, 160), "Hadley / Grayson / Colton / Tumbles", fill="#3b2918")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")


def validate_image(path: Path) -> None:
    with Image.open(path) as image:
        if image.format != "PNG" or image.size != IMAGE_SIZE:
            raise ValidationError(f"Illustration must be a {IMAGE_SIZE[0]}x{IMAGE_SIZE[1]} PNG")


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_story(payload: dict[str, Any], passage: dict[str, str], order: int, image_name: str) -> str:
    now = datetime.now(ZoneInfo("America/New_York"))
    offset = now.strftime("%z")
    offset = f"{offset[:3]}:{offset[3:]}"
    image_url = f"/ezra-blog/{IMAGE_DIR.as_posix()}/{image_name}"
    front = [
        "---",
        "layout: post",
        f"title: {yaml_quote(payload['title'])}",
        f"date: {now:%Y-%m-%d} 08:00:00 {offset}",
        f"image: {image_url}",
        f"excerpt: {yaml_quote(payload['excerpt'])}",
        "volume: 2",
        f"order: {order}",
        f"scripture: {yaml_quote(passage['reference'])}",
        "published: true",
        "---",
        "",
        f"![{payload['title']}]({image_url})",
        "",
    ]
    return "\n".join(front) + payload["body"].strip() + "\n"


def update_ledger(data: dict[str, Any], passage: dict[str, str], story_file: str, image_file: str) -> dict[str, Any]:
    updated = json.loads(json.dumps(data))
    updated["candidates"] = [item for item in updated["candidates"] if item["id"] != passage["id"]]
    updated["used"].append({
        "id": passage["id"],
        "reference": passage["reference"],
        "story_file": story_file,
        "image_file": image_file,
    })
    updated["used"] = sorted(updated["used"], key=lambda item: item["id"])
    return updated


def validate_repository(root: Path) -> None:
    ledger = load_ledger(root)
    used_refs = {canonical(item["reference"]): item for item in ledger["used"]}
    seen: dict[str, str] = {}
    for path in (root / STORY_DIR).glob("*.md"):
        meta = parse_front_matter(path)
        reference = meta.get("scripture")
        if not reference:
            continue
        key = canonical(str(reference))
        if key in seen:
            raise ValidationError(f"Duplicate scripture in {seen[key]} and {path.name}")
        seen[key] = path.name
        if meta.get("volume") == 2:
            for field in ("title", "date", "image", "excerpt", "order", "scripture"):
                if not meta.get(field):
                    raise ValidationError(f"{path.name} is missing {field}")
            if key not in used_refs:
                raise ValidationError(f"{path.name} scripture is absent from the passage ledger")
            local_image = str(meta["image"]).removeprefix("/ezra-blog/")
            if not (root / local_image).exists():
                raise ValidationError(f"{path.name} points to a missing illustration")
    for item in ledger["used"]:
        if not (root / item["story_file"]).exists():
            raise ValidationError(f"Ledger points to missing story: {item['story_file']}")
        if not (root / item["image_file"]).exists():
            raise ValidationError(f"Ledger points to missing image: {item['image_file']}")


def generate(source_root: Path, output_root: Path, mode: str, passage_id: str | None, metadata: Path | None) -> dict[str, Any]:
    ledger = load_ledger(source_root)
    passage = select_passage(ledger, passage_id)
    titles = existing_titles(source_root)
    payload = dry_payload(passage) if mode == "dry-run" else generate_story(passage, titles)
    validate_story(payload, passage, titles)
    slug = slugify(payload["title"])
    story_file = (STORY_DIR / f"{slug}.md").as_posix()
    image_file = (IMAGE_DIR / f"{slug}.png").as_posix()
    story_path = output_root / story_file
    image_path = output_root / image_file
    story_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "dry-run":
        placeholder_image(image_path)
    else:
        generate_image(image_path, payload["image_scene"])
    validate_image(image_path)
    story_path.write_text(render_story(payload, passage, next_order(source_root), image_path.name), encoding="utf-8")
    new_ledger = update_ledger(ledger, passage, story_file, image_file)
    ledger_out = output_root / LEDGER_PATH
    ledger_out.parent.mkdir(parents=True, exist_ok=True)
    ledger_out.write_text(json.dumps(new_ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result = {
        "mode": mode,
        "title": payload["title"],
        "passage_id": passage["id"],
        "reference": passage["reference"],
        "story_file": story_file,
        "image_file": image_file,
    }
    if metadata:
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if output_root.resolve() == source_root.resolve():
        validate_repository(output_root)
    print(json.dumps(result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("generate")
    make.add_argument("--source-root", type=Path, default=ROOT)
    make.add_argument("--output-root", type=Path, default=ROOT)
    make.add_argument("--mode", choices=("dry-run", "live"), default="dry-run")
    make.add_argument("--passage-id")
    make.add_argument("--metadata", type=Path)
    check = sub.add_parser("validate-repository")
    check.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    if args.command == "generate":
        generate(args.source_root.resolve(), args.output_root.resolve(), args.mode, args.passage_id, args.metadata)
    else:
        validate_repository(args.root.resolve())
        print("Kitty Chronicles repository validation passed.")


if __name__ == "__main__":
    main()
