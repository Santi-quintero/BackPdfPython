from PyPDF4 import PdfFileReader

def extraer_contenido_sigfield(pdf_path):
    campos_firma = []

    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        campos = pdf.getFields(tree=None, retval=None, fileobj=None)

        for key, value in campos.items():
            if value.get("/FT") == "/Sig":  # Check if it's a signature field
                campos_firma.append(value)

    return campos_firma

contenido = extraer_contenido_sigfield('./exports/final_signed_file1.pdf')

for firma in contenido:
    # print(firma)
    print("----------------------")
    print(f"Tipo de campo: {firma.get('/FT')}")
    print(f"Nombre del campo: {firma.get('/T')}")
    
    if firma.get('/V'):  # Si el campo de firma tiene un valor (está firmado)
        datos_firma = firma.get('/V')
        
        # A partir de aquí puedes extraer y visualizar más atributos del objeto 'datos_firma' si lo deseas
        if "/Name" in datos_firma:
            print(f"Nombre del firmante: {datos_firma['/Name']}")
        if "/ContactInfo" in datos_firma:
            print(f"Contacto del firmante: {datos_firma['/ContactInfo']}")
        if "/Reason" in datos_firma:
            print(f"Razon del firmante: {datos_firma['/Reason']}")
        if "/M" in datos_firma:
            print(f"fecha de la firma: {datos_firma['/M']}")
        if "/Location" in datos_firma:
            print(f"Location: {datos_firma['/Location']}")