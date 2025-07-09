import pytesseract
from pdf2image import convert_from_path, pdfinfo_from_path
import os
from PIL import Image, ImageSequence
import fitz
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\UL318UZ\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_text_from_scanned_pdf(pdf_path: str, save_images: bool = False) -> str:
    # Output folder for images (optional)
    output_image_folder = 'pdf_images'
    if save_images:
        os.makedirs(output_image_folder, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for i, image in enumerate(images):
        if save_images:
            image_path = os.path.join(output_image_folder, f'page_{i + 1}.png')
            image.save(image_path, 'PNG')

        text = pytesseract.image_to_string(image, lang='eng')
        full_text += f"\n--- Page {i + 1} ---\n{text}\n"

    return full_text

def extract_text_from_tiff(tiff_path: str) -> str:
    text = ""
    with Image.open(tiff_path) as img:
        for i, page in enumerate(ImageSequence.Iterator(img)):
            page_text = pytesseract.image_to_string(page, lang='eng')
            text += f"\n--- Page {i+1} ---\n{page_text}\n"
    return text

def check_pdf_image_dpi(pdf_path: str, min_required_dpi=72):
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc):
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Load with Pillow
            image = Image.open(io.BytesIO(image_bytes))
            dpi_info = image.info.get("dpi")

            if dpi_info:
                dpi_x, dpi_y = dpi_info
                if dpi_x < min_required_dpi and dpi_y < min_required_dpi:
                    raise ValueError(
                        f"Page {page_num + 1}: Image DPI too low ({dpi_x}x{dpi_y}). Minimum required is {min_required_dpi} DPI."
                    )
            else:
                # Fallback to pixel-based estimation using page dimensions (less reliable)
                width_px = image.width
                height_px = image.height
                bbox = page.rect
                width_in = bbox.width / 72
                height_in = bbox.height / 72

                dpi_x = width_px / width_in
                dpi_y = height_px / height_in

                if dpi_x < min_required_dpi and dpi_y < min_required_dpi:
                    raise ValueError(
                        f"Minimum required is {min_required_dpi} DPI."
                        f"Page {page_num + 1}: Estimated DPI too low ({int(dpi_x)}x{int(dpi_y)}). "
                    )
    return True

def send_outlook_email(subject: str, body: str, recipients: list, cc: list = None, preview_only=False):
    import win32com.client as win32
    import pythoncom
    import time

    pythoncom.CoInitialize()
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)

        mail.Subject = subject
        mail.Body = body
        mail.To = ";".join(recipients)
        if cc:
            mail.CC = ";".join(cc)

        time.sleep(1)  # Give Outlook a moment

        # mail.Display()
        mail.Send()

    except Exception as e:
        print(f"❌ Outlook send failed: {e}")
        raise
    finally:
        pythoncom.CoUninitialize()  