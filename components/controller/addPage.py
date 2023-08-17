import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import PyPDF4
import base64


def base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)


def agregar_nueva_pagina(base64_pdf):
    # Decodificar el Base64 a bytes
    pdf_bytes = base64_to_bytes(base64_pdf)

    # Abrir el PDF existente en modo lectura
    existing_pdf = PyPDF4.PdfFileReader(io.BytesIO(pdf_bytes))
    output_pdf = PyPDF4.PdfFileWriter()

    # Agregar las páginas existentes al PDF de salida
    for page_num in range(existing_pdf.getNumPages()):
        page = existing_pdf.getPage(page_num)
        output_pdf.addPage(page)

    # Crear una nueva página con el mismo tamaño que las páginas existentes
    page = existing_pdf.getPage(0)
    nueva_pagina = PyPDF4.pdf.PageObject.createBlankPage(width=page.mediaBox.getWidth(), height=page.mediaBox.getHeight())

    # Agregar el contenido "Firmas Digitales" centrado en la parte superior central
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    text = "Firmas Digitales"
    c.setFont("Helvetica-Bold", 24)
    text_width = c.stringWidth(text, "Helvetica-Bold", 24)
    text_height = 1
    c.drawString((letter[0] - text_width) / 2, letter[1] - text_height, text)
    c.save()

    # Mover el puntero al principio del archivo en el stream de bytes
    packet.seek(0)
    new_pdf = PyPDF4.PdfFileReader(packet)
    nueva_pagina.mergePage(new_pdf.getPage(0))
    # Agregar la nueva página al PDF de salida
    output_pdf.addPage(nueva_pagina)

    # Obtener el PDF resultante en bytes (Uint8Array)
    output_bytes = io.BytesIO()
    output_pdf.write(output_bytes)
    return output_bytes.getvalue()


# base64_pdf = ""  # Aquí colocas tu Base64 del PDF
# result_bytes = agregar_nueva_pagina(base64_pdf)

# with open("./exports/output.pdf", "wb") as output_file:
#     output_file.write(result_bytes)

