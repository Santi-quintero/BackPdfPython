
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms


def firmar(firma_x, firma_y, firmante, output_file):
    contraseña = "Luis43.%"
    certificado_path = "./assets/LuizGonzalez.pfx"
    # contraseña = "Sq1234%."
    # certificado_path = "./assets/SantiQuintero.pfx"
    pdf_path = "./assets/PoderAsambleaAccionistasCCARENDIR.pdf"

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date_str = date.strftime("D:%Y%m%d%H%M%S+00'00'")

    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (firma_x, firma_y, firma_x + 200, firma_y - 90),  # Ajusta estos valores como sea necesario
        #"signature": f"Firmado digitalmente por {firmante} el {date.strftime('%Y-%m-%d')}",
        "signature_img": "./assets/codigo1.png",
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
firmar(70, 440, 'John Doe', './exports/documento_firmado.pdf');



