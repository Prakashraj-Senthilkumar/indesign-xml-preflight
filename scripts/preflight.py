"""CLI: python scripts/preflight.py samples/article.xml config/style-map.example.json"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from preflight import check  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight journal XML")
    parser.add_argument("xml", type=Path)
    parser.add_argument("style_map", type=Path)
    args = parser.parse_args()
    report = check(args.xml, args.style_map)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
