import base64
import io
from flask import Flask, request, jsonify, send_file

from components.controller.addPage import agregar_nueva_pagina
from components.controller.pruebaValid import extraer_contenido_sigfield
from components.controller.sign import firmar
from components.controller.signNotaries import firmarNotarie
from components.controller.validSign import verify_pdf_signature


app = Flask(__name__)



@app.route('/addPage',  methods=['POST'])
def addPage():
    # Obtener los datos del JSON enviado por el cliente
    data = request.json
    pdf_base64 = data.get("PDF")
    try:
        # Llamar a la función de agregar_nueva_pagina para añadir la nueva página al PDF
        pdf_con_nueva_pagina_bytes = agregar_nueva_pagina(pdf_base64)
        resultado_bytes = pdf_con_nueva_pagina_bytes


        # Convertir el resultado_bytes a un Uint8Array (Lista de enteros de 8 bits sin signo)
        uint8_array = list(resultado_bytes)

         # Crear un diccionario que contiene el statusCode y el Uint8Array
        response_data = {
            "statusCode": 200,
            "body": uint8_array
        }

        # Enviar el JSON como respuesta al cliente
        return jsonify(response_data)
    except ValueError as e:
        # Si ocurre un error, devolver un JSON con el mensaje de error
        return jsonify({"statusCode": 500, "error": str(e)})
    
@app.route('/sign', methods=['POST'])
def sign():
    # Obtener los datos del JSON enviado por el cliente
    data = request.json
    pdf_base64 = data.get("PDF")

    try:
        # countSignature =0;
        # Iterar sobre cada firma en el objeto de firmas
        for signature_data in data.get("signatures"):
            position = signature_data.get("position")
            signature = signature_data.get("signature")

            # Llamar a la función de firmar para firmar el PDF
            uint8_array = firmar(signature, pdf_base64, position)

            # Convierte el uint8_array a bytes
            byte_data = bytes(uint8_array)

            # Convierte el PDF firmado de uint8_array a base64 para la siguiente iteración
            pdf_base64 = base64.b64encode(byte_data).decode()
            # countSignature= countSignature + 1
 # Convierte el uint8_array a bytes
        byte_data = bytes(uint8_array)
        # Crear un diccionario que contiene el statusCode y el Uint8Array
        response_data = {
            "statusCode": 200,
            "body": uint8_array  # PDF firmado final
        }

        # Enviar el JSON como respuesta al cliente
        return jsonify(response_data)
    except ValueError as e:
        # Si ocurre un error, devolver un JSON con el mensaje de error
        return jsonify({"statusCode": 500, "error": str(e)})

    
@app.route('/signNotaries', methods=['POST'])
def signNotaries():
 # Obtener los datos del JSON enviado por el cliente
    data = request.json
    pdf_base64 = data.get("PDF")
    # rectX = data.get("X")
    # rectY = data.get("Y")
    try:

        # Llamar a la función de firmar para firmar el PDF
        uint8_array = firmarNotarie('Santiago quintero', pdf_base64)

         # Crear un diccionario que contiene el statusCode y el Uint8Array
        response_data = {
            "statusCode": 200,
            "body": uint8_array
        }

        # Enviar el JSON como respuesta al cliente
        return jsonify(response_data)
    except ValueError as e:
        # Si ocurre un error, devolver un JSON con el mensaje de error
        return jsonify({"statusCode": 500, "error": str(e)})
    
@app.route('/verifyPdf', methods=['POST'])
def verifyPdf():
 # Obtener los datos del JSON enviado por el cliente
    data = request.json
    pdf_base64 = data.get("PDF")
    # rectX = data.get("X")
    # rectY = data.get("Y")
    try:

        # Llamar a la función de validar el pdf
        response = verify_pdf_signature(pdf_base64)

         # Crear un diccionario que contiene el statusCode y el Uint8Array
        response_data = {
            "statusCode": 200,
            "body": response
        }

        # Enviar el JSON como respuesta al cliente
        return jsonify(response_data)
    except ValueError as e:
        # Si ocurre un error, devolver un JSON con el mensaje de error
        return jsonify({"statusCode": 500, "error": str(e)})
    
@app.route('/extractSignatureInfo', methods=['POST'])
def extract_signature_info():
    try:
        # Obtener los datos del JSON enviado por el cliente
        data = request.json
        pdf_base64 = data.get("PDF")

        # Llamar a la función extraer_contenido_sigfield para extraer la información de firma del PDF
        signature_info_list = extraer_contenido_sigfield(pdf_base64)

        # Crear un diccionario que contiene el statusCode y la lista con la información de firma
        response_data = {
            "statusCode": 200,
            "body": signature_info_list
        }

        # Enviar el JSON como respuesta al cliente
        return jsonify(response_data)

    except ValueError as e:
        # Si ocurre un error, devolver un JSON con el mensaje de error
        return jsonify({"statusCode": 500, "error": str(e)})

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=81, debug=True)

