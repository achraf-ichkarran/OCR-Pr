from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import time
import os

# 🧠 Renseigne ta clé et ton endpoint ici :
endpoint = "https://ocr-main.cognitiveservices.azure.com/"
key = "9YvfQeXOHJoI4al7dKKvEGBHma1LiQnew6P4k93t21K90Bjr3or5JQQJ99BFAC5T7U2XJ3w3AAAFACOGqTP6"

# 📷 Sélection du fichier image localement
image_path = input("Entrez le chemin de l'image (ex: ./images/photo.jpg) : ")

# Vérifie si le fichier existe
if not os.path.exists(image_path):
    print("❌ Fichier introuvable.")
    exit()

with open(image_path, "rb") as image_stream:
    # 🔍 Création du client
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

    # 📖 Lance la lecture OCR manuscrite
    read_op = client.read_in_stream(image_stream, language="fr", raw=True)
    operation_location = read_op.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # ⏳ Attente des résultats
    while True:
        result = client.get_read_result(operation_id)
        if result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)

    # 📄 Affichage du texte
    if result.status.lower() == 'succeeded':
        for page in result.analyze_result.read_results:
            for line in page.lines:
                print(line.text)
    else:
        print("❌ Échec de l'OCR.")
