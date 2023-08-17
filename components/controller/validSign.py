import json
import base64
from endesive import pdf

def verify_pdf_signature(pdf_base64):
    """
    Función para verificar una firma digital en un PDF.
    """

    # Decodificar el archivo PDF desde base64
    data = base64.b64decode(pdf_base64)

    # Verificar las firmas digitales
    results = pdf.verify(data)  

    response = {}

    # Si la lista de resultados está vacía, no hay firmas en el documento
    if not results:
        response['valid'] = False
        response['message'] = "El documento no tiene firmas."
        return json.dumps(response)
    
    print(results)
    valid_signatures = 0
    invalid_signatures = 0

    # Para cada resultado en los resultados
    for i, result in enumerate(results):
        unchanged, valid_signature, _ = result
        print(unchanged)
        print(valid_signature)

        # Si el contenido del PDF no ha cambiado y la firma es válida
        if unchanged and valid_signature:
            valid_signatures += 1
        else:
            invalid_signatures += 1

    response['valid'] = True if valid_signatures > 0 and invalid_signatures == 0 else False
    response['message'] = f"El documento tiene {valid_signatures} firma(s) válida(s) y {invalid_signatures} firma(s) inválida(s)."

    return json.dumps(response)

# Llamar a la función con el archivo PDF en base64 que deseas verificar
# with open("./exports/santi.pdf", "rb") as file:
#     pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
pdf_base64=""
print(verify_pdf_signature(pdf_base64))
