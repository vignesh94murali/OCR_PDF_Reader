import fitz  # PyMuPDF

doc = fitz.open(r"C:\Users\UL318UZ\Downloads\Cover Story.pdf")
new_pdf = fitz.open()

for page in doc:
    pix = page.get_pixmap(dpi=72)  # reduce DPI to lower quality
    img_pdf = fitz.open("pdf", pix.tobytes("pdf"))
    new_pdf.insert_pdf(img_pdf)

new_pdf.save("output_low_quality.pdf")
