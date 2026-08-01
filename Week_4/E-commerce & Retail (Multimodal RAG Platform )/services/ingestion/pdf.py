import pymupdf4llm


def extract_pdf(file_path: str) -> str:
    text = pymupdf4llm.to_markdown(file_path)

    return [text]