import json
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parent
metadata = root / "summary.json"
output_path = root / "outputs"


def convert_mistral(filepath: Path) -> None:
    with filepath.open("r", encoding="utf-8") as f:
        data = json.load(f)
    content = ""
    for page in data["pages"]:
        content += page["markdown"]

    with open(output_path / f"{filepath.stem}.md", "w", encoding="utf-8") as f:
        f.write(content)


def main() -> int:
    with metadata.open("r", encoding="utf-8") as f:
        summary = json.load(f)
    data = pd.DataFrame(summary)
    data["id"] = data["new_name"].str.split(".pdf").str[0].astype(int)

    for f in output_path.rglob("mistral*.json"):
        convert_mistral(f)

    parsed = []
    for md in output_path.rglob("*.md"):
        content = md.read_text(encoding="utf-8")
        if "deepseek" in md.stem or "nanonets" in md.stem:
            parts = md.stem.split("-")
            model = f"{parts[0]}-{parts[1]}"
            document = int(parts[-1].split(".md")[0])
        elif "docling" in md.stem or "mistral" in md.stem:
            model, document = md.stem.split("-")
            document = int(document.split(".md")[0])
        else:
            raise ValueError("Unexpected format")
        parsed.append({"id": document, "tool": model, "content": content})

    docs = pd.DataFrame(parsed)
    pd.merge(docs, data, on="id", how="left").to_excel(
        root / "results.xlsx", index=False
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
