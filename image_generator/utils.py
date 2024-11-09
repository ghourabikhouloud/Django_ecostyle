# image_generator/utils.py
from django.conf import settings
import os

import torch
from diffusers import StableDiffusionPipeline

# Charger le modèle Stable Diffusion
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id)

# Déplacer le modèle vers le CPU
pipe = pipe.to("cpu")

# Utiliser une option pour exécuter le modèle en mode hors GPU et réduire la consommation de RAM.
pipe.enable_attention_slicing()  # Optimisation p

# Function to generate an image from a description
def generate_image(description):
    # image = pipe(description).images[0]
    # image_path = "generated_image.png"
    # image.save(image_path)
    # return image_path
    image = pipe(description).images[0]
    
    # Créer un nom de fichier unique pour chaque image
    image_filename = f"{description.replace(' ', '_')}.png"
    
    # Créer le chemin complet pour sauvegarder l'image
    image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
    
    # Sauvegarder l'image
    image.save(image_path)
    
    # Retourner le chemin d'accès à l'image pour l'afficher
    return f"{settings.MEDIA_URL}{image_filename}"