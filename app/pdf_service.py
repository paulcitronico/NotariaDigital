import os
from io import BytesIO
from flask import render_template, current_app

try:
    from xhtml2pdf import pisa
    XHTML2PDF_AVAILABLE = True
except Exception:
    XHTML2PDF_AVAILABLE = False

def generate_copy_file(document, office):
    html = render_template("documents/copy_template.html", document=document, office=office)

    if XHTML2PDF_AVAILABLE:
        filename = f"copia_{document.verification_code}.pdf"
        output_path = os.path.join(current_app.config["UPLOAD_FOLDER_COPIES"], filename)

        with open(output_path, "wb") as result_file:
            pisa_status = pisa.CreatePDF(
                src=BytesIO(html.encode("utf-8")),
                dest=result_file,
                encoding="utf-8"
            )

        if not pisa_status.err:
            return filename

    filename = f"copia_{document.verification_code}.html"
    output_path = os.path.join(current_app.config["UPLOAD_FOLDER_COPIES"], filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return filename