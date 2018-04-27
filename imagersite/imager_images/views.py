from django.shortcuts import render, redirect
from .models import Photo


def photos_view(request):
    photo = Photo.objects.all().filter(published='PUBLIC')
    photos = {
        'photos': photo
    }
    if photos:
        return render(request, 'generic/home.html', photos)



