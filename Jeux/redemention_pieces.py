# fichier utiliser pour redimentionner les pièces la première fois pour les mettre toute en 60x60 px

from PIL import Image
import os

input_folder = "../pieces/"
output_folder = "pieces_resized/"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(input_folder, filename))
        img = img.resize((60, 60), Image.LANCZOS)  # Redimensionne en 60x60 px
        img.save(os.path.join(output_folder, filename)) 

print("✅ Redimensionnement terminé !")
