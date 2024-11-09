from django.shortcuts import render
from django.views import View
from .utils import generate_image  # Ensure this function exists

class GenerateImageView(View):
    def get(self, request):
        return render(request, 'generate_image.html')

    def post(self, request):
        description = request.POST.get("description")
        if not description:
            return render(request, 'generate_image.html', {"error": "No description provided"})
        try:
            image_path = generate_image(description)
            return render(request, 'generate_image.html', {"image_path": image_path, "description": description})
        except Exception as e:
            return render(request, 'generate_image.html', {"error": str(e)})
