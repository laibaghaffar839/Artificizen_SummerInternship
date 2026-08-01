from PIL import Image
import pytesseract


def extract_image(file_path: str) -> list[str]:
    """
    Extract text from an image using OCR.
    """

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    text = text.strip()

    if not text:
        return []

    return [text]