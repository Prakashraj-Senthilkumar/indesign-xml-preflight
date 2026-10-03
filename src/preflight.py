"""Preflight journal XML before InDesign import."""

from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Any


def check(xml_path: Path, style_map_path: Path) -> dict[str, Any]:
    allowed = set(json.loads(style_map_path.read_text(encoding="utf-8"))["allowed_styles"])
    errors: list[str] = []
    warnings: list[str] = []

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        return {"file": str(xml_path), "ok": False, "errors": [f"parse error: {exc}"], "warnings": []}

    root = tree.getroot()
    if root.tag != "article":
        errors.append(f"root is {root.tag!r}, expected 'article'")

    title = root.find("./front/article-meta/title-group/article-title")
    if title is None or not (title.text or "").strip():
        errors.append("missing or empty article-title")

    sections = root.findall("./body/sec")
    if not sections:
        errors.append("body has no sec")

    for node in root.iter():
        style = node.attrib.get("style")
        if style and style not in allowed:
            errors.append(f"style {style!r} on <{node.tag}> is not in the style map")
        if node.tag == "xref" and not node.attrib.get("rid"):
            errors.append("xref missing rid")

    return {
        "file": str(xml_path),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }
