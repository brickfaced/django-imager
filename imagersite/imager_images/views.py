from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album, User
from imager_profile.models import ImagerProfile
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse


class PhotosView(TemplateView):
    template_name = 'imager_images/photos.html'

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        photos = Photo.objects.all().filter(published='PUBLIC')
        if photos.count():
            context = {'photos': photos}
            return context


class AlbumsView(TemplateView):
    template_name = 'imager_images/albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        albums = Album.objects.all().filter(published='PUBLIC')
        if albums.count():
            context = {
                'albums': albums
                }
            return context


class LibraryView(TemplateView):
    template_name = 'imager_images/library.html'
    context_object_name = 'library'

    def get(self, *args, **kwargs):
        """something here"""
        if not self.request.user.get_username():
            return redirect('home')
        self.username = self.request.user.get_username()
        return super().get(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """query all allbums"""
        photos = Photo.objects.all().filter(published='PUBLIC')
        albums = Album.objects.all().filter(published='PUBLIC')
        context = {
            'albums': albums,
            'photos': photos,
            }
        return context


class PhotoView(DetailView):
    template_name = 'imager_images/photo.html'
    context_object_name = 'single_photo'

    def get(self, *args, **kwargs):
        """something here"""
        if not self.request.user.get_username():
            return redirect('home')
        self.username = self.request.user.get_username()
        return super().get(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        if self.kwargs[id]:
            photo_id = self.kwargs[id]
            photo = get_object_or_404(Photo, id=photo_id)
            context = {
                'photo': {'thumb': photo, 'link': reverse('photos')}
                }
        return context




def photo_view(request, photo_id=None):
    
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': [{'cover': album.cover, 'link': reverse('album',
                    args=[album.id])} for album in albums],
        'photos': [{'thumb': photo, 'link': reverse('photos', args=[photo.id])} for photo in photos]
    }
    return render(request, 'imager_images/photo.html', context)


def _album_with_cover(photos, cover):
    if cover is not None:
        return set(photos) | {cover}
    return photos


def album_view(request, album_id=None):
    """Album View."""
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
    }
    if album_id:
        album = get_object_or_404(Album, id=album_id)
        context["photos"] = _album_with_cover(Photo.objects.filter(album__id=album.id).filter(published='PUBLIC'), album.cover)
        context["album"] = album
        return render(request, 'imager_images/album.html', context)
    return render(request, 'imager_images/album.html', context)
