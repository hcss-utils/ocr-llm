from pathlib import Path
from docling.document_converter import DocumentConverter

root = Path(__file__).resolve().parent
input_path = root / "data"
output_path = root / "outputs"

if __name__ == "__main__":
    for filename in input_path.rglob("*.pdf"):
        converter = DocumentConverter()
        contents = converter.convert(filename).document
        if contents:
            output_filename = output_path / f"docling-{filename.stem}.md"
            with output_filename.open("w") as f:
                f.write(contents.export_to_markdown())
