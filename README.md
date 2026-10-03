# indesign-xml-preflight

Checks journal XML before it is imported into InDesign.

A file passes only when required elements exist, every mapped style name is declared, and there are no empty required text nodes. Failures are written as JSON so a batch runner can stop or quarantine the manuscript.

Pairs with [word-to-xml-bulk-converter](https://github.com/Prakashraj-Senthilkumar/word-to-xml-bulk-converter) and [macro-layouts-orchestrator](https://github.com/Prakashraj-Senthilkumar/macro-layouts-orchestrator).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/preflight.py samples/article.xml config/style-map.example.json
```

Exit code `0` means pass. Exit code `1` means one or more errors. Warnings do not fail the run.

## Checks

- Root element is `article`
- `front/article-meta/title-group/article-title` is present and non-empty
- At least one `body/sec` exists
- Every `style` attribute value is listed in the style map
- No `xref` without a `rid`

Edit `config/style-map.example.json` to match the paragraph and character styles in the InDesign template. Do not hard-code style names in the checker.
