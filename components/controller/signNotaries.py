
import datetime
import base64
from io import BytesIO
import io
from PyPDF4 import PdfFileReader
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms

def bytes_to_uint8array(data_bytes):
    return list(data_bytes)

def obtieneUltimaPagina(pdf_base64):
    # Decodificar el PDF de formato Base64 a bytes
    pdf_bytes = base64.b64decode(pdf_base64)
    
    # Leer el PDF desde los bytes
    pdf = PdfFileReader(io.BytesIO(pdf_bytes))

    num_pagina = pdf.getNumPages() - 1

    return num_pagina

def firmarNotarie(firmante, pdf_base64):
    contraseña = "Sq1234%."
    certificado_path = "./assets/SantiQuintero.pfx"

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date_str = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    # Contenido del texto que deseas agregar
    firma_texto = f"""Firmado Digitalmente por:
    {firmante}
    Fecha: {date_str}
    Nombre Notaria: Notaria Primera de Bogota
    Direccion Notaria: Calle 16 No. 4 - 62, Notaria
    1 Bogotá Cundinamarca"""
    num_firmas_existentes = 1
    page = obtieneUltimaPagina(pdf_base64);
    altura_firma = 80
    margen = 5

    dct = {
            "aligned": 0,
            "sigflags": 3,
            "sigflagsft": 132,
            "sigpage": page,
            "sigbutton": True,
            "sigfield": "SignatureNotarie",
            # "auto_sigfield": False,
            # "sigandcertify": False,
            "signaturebox": (
            70, 
            700 - num_firmas_existentes * (altura_firma + margen), 
            320, 
            780 - num_firmas_existentes * (altura_firma + margen)
            ),  
            #"signature": f"Firmado digitalmente por {firmante} el {date.strftime('%Y-%m-%d')}",
            "signature_manual": [
                #                R     G     B
                ['fill_colour', 0.95, 0.95, 0.95],

                #            *[bounding box]
                ['rect_fill', 0, 0, 0, 0],

                #                  R    G    B
                ['stroke_colour', 0.8, 0.8, 0.8],

                #        inset
                ['border', 2],

                #          key  *[bounding box]  distort centred
                ['image', 'sig0', 5, 5, 100, 75,  False, False],

                #         font     fs 
                ['font', 'default', 8],
                #               R  G  B
                ['fill_colour', 0, 0, 0],

                #            text
                ['text_box', firma_texto,
                    # font  *[bounding box], fs, wrap, align, baseline
                    'default', 80, 2, 195, 77, 8, True, 'left', 'top'],
                ],
            #   key: name used in image directives
            # value: PIL Image object or path to image file
            "manual_images": {'sig0': './assets/codigo1.png'},
            "manual_fonts": {},
            "contact": "hola@ejemplo.com",
            "location": "Ubicación",
            "signingdate": date_str,
            "reason": "Razón",
            "password": contraseña,
        }

    with open(certificado_path, "rb") as certificado:
        p12 = pkcs12.load_key_and_certificates(
            certificado.read(), contraseña.encode("ascii"), backends.default_backend()
        )
    
    # Convertir el PDF en formato Base64 a bytes
    pdf_bytes = base64.b64decode(pdf_base64)
    
    # Firmar el PDF
    datau = pdf_bytes
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    
    # Combinar los bytes de PDF con los de la firma
    resultado_bytes = BytesIO()
    resultado_bytes.write(datau)
    resultado_bytes.write(datas)
    resultado_bytes.seek(0)
    
    # Convertir los bytes en un Uint8Array (lista de enteros de 8 bits sin signo)
    uint8_array = bytes_to_uint8array(resultado_bytes.getvalue())
    
    return uint8_array

# # Ejemplo de uso
# pdf_base64 = ""  # Aquí colocas el Base64 del PDF que deseas firmar
# resultado_uint8array = firmar('Santiago quintero2asdasds', pdf_base64)
# # print(resultado_uint8array)


# with open("./exports/outputsss.pdf", "wb") as output_file:
#     output_file.write(bytes(resultado_uint8array))


# import datetime
# import base64
# from cryptography.hazmat import backends
# from cryptography.hazmat.primitives.serialization import pkcs12
# from endesive.pdf import cms

# def firmar(firmante, pdf_base64):
#     contraseña = "Sq1234%."
#     certificado_path = "./assets/SantiQuintero.pfx"

#     date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
#     date_str = date.strftime("D:%Y%m%d%H%M%S+00'00'")

#     firma_texto = f"""Firmado Digitalmente por:
#     {firmante}
#     Fecha: {date_str}
#     Nombre Notaria: Notaria Primera de Bogota
#     Direccion Notaria: Calle 16 No. 4 - 62, Notaria
#     1 Bogotá Cundinamarca"""

#     num_firmas_existentes = 1
#     altura_firma = 80
#     margen = 5

#     dct = {
#             "aligned": 0,
#             "sigflags": 3,
#             "sigflagsft": 132,
#             "sigpage": 0,
#             "sigbutton": True,
#             "sigfield": "Signature1",
#             # "auto_sigfield": False,
#             # "sigandcertify": False,
#             "signaturebox": (
#             70, 
#             700 - num_firmas_existentes * (altura_firma + margen), 
#             320, 
#             780 - num_firmas_existentes * (altura_firma + margen)
#             ),  
#             #"signature": f"Firmado digitalmente por {firmante} el {date.strftime('%Y-%m-%d')}",
#             "signature_manual": [
#                 #                R     G     B
#                 ['fill_colour', 0.95, 0.95, 0.95],

#                 #            *[bounding box]
#                 ['rect_fill', 0, 0, 0, 0],

#                 #                  R    G    B
#                 ['stroke_colour', 0.8, 0.8, 0.8],

#                 #        inset
#                 ['border', 2],

#                 #          key  *[bounding box]  distort centred
#                 ['image', 'sig0', 5, 5, 100, 75,  False, False],

#                 #         font     fs 
#                 ['font', 'default', 8],
#                 #               R  G  B
#                 ['fill_colour', 0, 0, 0],

#                 #            text
#                 ['text_box', firma_texto,
#                     # font  *[bounding box], fs, wrap, align, baseline
#                     'default', 80, 2, 195, 77, 8, True, 'left', 'top'],
#                 ],
#             #   key: name used in image directives
#             # value: PIL Image object or path to image file
#             "manual_images": {'sig0': './assets/codigo1.png'},
#             "manual_fonts": {},
#             "contact": "hola@ejemplo.com",
#             "location": "Ubicación",
#             "signingdate": date_str,
#             "reason": "Razón",
#             "password": contraseña,
#         }

#     with open(certificado_path, "rb") as certificado:
#         p12 = pkcs12.load_key_and_certificates(
#             certificado.read(), contraseña.encode("ascii"), backends.default_backend()
#         )
    
#     pdf_bytes = base64.b64decode(pdf_base64)
#     datas = cms.sign(pdf_bytes, dct, p12[0], p12[1], p12[2], "sha256")
    
#     return datas  # Return the signed PDF data directly

# pdf_base64 = ""  # Aquí colocas el Base64 del PDF que deseas firmar
# resultado_bytes = firmar('Santiago quintero2asdasds', pdf_base64)

# with open("./exports/outputsss.pdf", "wb") as output_file:
#     output_file.write(resultado_bytes)
