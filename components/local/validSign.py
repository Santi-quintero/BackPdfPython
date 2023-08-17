from endesive import pdf

def verify_pdf_signature(pdf_file_path):
    """
    Función para verificar una firma digital en un PDF.
    """

    # Leer el archivo PDF
    with open(pdf_file_path, "rb") as file:
        data = file.read()

    # Verificar las firmas digitales
    results = pdf.verify(data)

    # Si la lista de resultados está vacía, no hay firmas en el documento
    if not results:
        print("El documento no tiene firmas.")
        return

    # Para cada resultado en los resultados
    for i, result in enumerate(results):
        unchanged, valid_signature, _ = result

        # Si el contenido del PDF no ha cambiado y la firma es válida
        if unchanged and valid_signature:
            print(f"Firma {i+1} es válida.")
        else:
            print(f"Firma {i+1} no es válida.")

# Llamar a la función con la ruta al archivo PDF que deseas verificar
verify_pdf_signature("./exports/sign8.pdf")
