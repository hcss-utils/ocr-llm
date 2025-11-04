import base64
import os
from pathlib import Path

from mistralai import Mistral, OCRResponse

root = Path(__file__).resolve().parent
input_path = root / "data"
output_path = root / "outputs"

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])


def llm_ocr(client: Mistral, pdf_path: Path) -> OCRResponse:
    """
    Perform OCR on a PDF via Mistral LLM.

    Reads the PDF, encodes it to base64, and sends it to the OCR endpoint.

    Parameters
    ----------
    client : Mistral
        Configured Mistral client for OCR processing.
    pdf_path : Path
        Path to the input PDF file.

    Returns
    -------
    OCRResponse
        The raw OCR response containing markdown and images.
    """
    base64_pdf = _encode_pdf(pdf_path)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}",
        },
        include_image_base64=True,
    )
    return ocr_response


def _encode_pdf(pdf_path: Path) -> str | None:
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main() -> int:
    """Main entry point"""
    for filename in input_path.rglob("*.pdf"):
        contents = llm_ocr(client=client, pdf_path=filename)
        if contents:
            output_filename = output_path / f"{filename.stem}.json"
            with output_filename.open("w") as f:
                f.write(contents.model_dump_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
