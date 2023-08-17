
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms


def firmar(firma_x, firma_y, firmante, output_file):
    # contraseña = "Luis43.%"
    # certificado_path = "./assets/LuizGonzalez.pfx"
    contraseña = "Sq1234%."
    certificado_path = "./assets/SantiQuintero.pfx"
    pdf_path = "./exports/sign7.pdf"
    # pdf_path = "./assets/PoderAsambleaAccionistasCCARENDIR.pdf"

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date_str = date.strftime("D:%Y%m%d%H%M%S+00'00'")
# Contenido del texto que deseas agregar
    firma_texto = f"""Firmado Digitalmente por:
    {firmante}
    Fecha: {date_str}
    Nombre Notaria: Notaria Primera de Bogota
    Direccion Notaria: Calle 16 No. 4 - 62, Notaria
    1 Bogotá Cundinamarca"""
    num_firmas_existentes = 2

    altura_firma = 80
    margen = 5

    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature2",
        "auto_sigfield": False,
        "sigandcertify": False,
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

    with open(certificado_path, "rb") as certificado, open(pdf_path, "rb") as pdf:
        p12 = pkcs12.load_key_and_certificates(
            certificado.read(), contraseña.encode("ascii"), backends.default_backend()
        )
        datau = pdf.read()
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

    with open(output_file, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
firmar(70, 440, 'Santiago quintero2asdasds', './exports/sign8.pdf');


