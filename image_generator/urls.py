# image_generator/urls.py

from django.urls import path
from .views import GenerateImageView

app_name = 'image_generator'  # Assurez-vous d'avoir défini app_name

urlpatterns = [
    path('', GenerateImageView.as_view(), name='generate_image'),
]
