import base64
from io import BytesIO
from PyPDF4 import PdfFileReader

def extraer_contenido_sigfield(pdf_base64):
    campos_firma = []
    lista_firmas = []

    # Decodificamos la cadena base64 a bytes
    pdf_bytes = base64.b64decode(pdf_base64)

    # Utilizamos BytesIO para tratar los bytes decodificados como un archivo
    pdf_buffer = BytesIO(pdf_bytes)

    pdf = PdfFileReader(pdf_buffer)
    campos = pdf.getFields(tree=None, retval=None, fileobj=None)

    for key, value in campos.items():
        if value.get("/FT") == "/Sig":  # Check if it's a signature field
            campos_firma.append(value)

    for firma in campos_firma:
        firma_info = {}
        firma_info["Tipo de campo"] = firma.get('/FT')
        firma_info["Nombre del campo"] = firma.get('/T')

        if firma.get('/V'):  # Si el campo de firma tiene un valor (está firmado)
            datos_firma = firma.get('/V')

            if "/Name" in datos_firma:
                firma_info["Nombre del firmante"] = datos_firma['/Name']
            if "/ContactInfo" in datos_firma:
                firma_info["Contacto del firmante"] = datos_firma['/ContactInfo']
            if "/Reason" in datos_firma:
                firma_info["Razon del firmante"] = datos_firma['/Reason']
            if "/M" in datos_firma:
                firma_info["fecha de la firma"] = datos_firma['/M']
            if "/Location" in datos_firma:
                firma_info["Location"] = datos_firma['/Location']

        lista_firmas.append(firma_info)

    # Si no hay firmas, retornamos un mensaje
    if not lista_firmas:
        return ["El PDF no tiene firmas."]
    
    return lista_firmas

# # Uso de la función:
# pdf_base64_string = "TU_CADENA_BASE64_AQUÍ"
# contenido = extraer_contenido_sigfield(pdf_base64_string)

# # Si deseas imprimir la lista para visualizarla:
# for firma_info in contenido:
#     if isinstance(firma_info, str):  # Si es una cadena (mensaje)
#         print(firma_info)
#     else:  # Si es un diccionario con información de firma
#         for key, value in firma_info.items():
#             print(f"{key}: {value}")
#         print("----------------------")
