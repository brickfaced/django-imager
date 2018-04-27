from django.shortcuts import render
from imager_images.models import Photo


def home_view(request):
    photos = Photo.objects.all().filter(published='PUBLIC')
    context = {
        'photos': photos
    }
    if photos:
        return render(request, 'generic/home.html', context)
    new = 'sdfsdfsdf'
    return render(request, 'generic/home.html', {'message': new})
