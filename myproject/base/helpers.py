import io
import os

from django.core.files.base import ContentFile
from pdf2image import convert_from_path


def extract_first_page_of_pdf_as_image(pdf_path, output_name = None):
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)
    first_page = pages[0]

    # Convert image to bytes
    img_io = io.BytesIO()
    first_page.save(img_io, format='JPEG')
    img_io.seek(0)

    if output_name:
        filename = f"{output_name}.jpg"
    else:
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        filename = f"{base}_cover.jpg"

    return filename, ContentFile(img_io.read())

