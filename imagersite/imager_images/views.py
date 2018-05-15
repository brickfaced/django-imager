from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album, User
from imager_profile.models import ImagerProfile
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from random import sample


class PhotosView(LoginRequiredMixin, TemplateView):
    template_name = 'imager_images/photos.html'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('photos')

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        photos = Photo.objects.all().filter(published='PUBLIC')
        if photos.count():
            context = {'photos': photos}
            return context


class AlbumsView(LoginRequiredMixin, TemplateView):
    template_name = 'imager_images/albums.html'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('albums')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        albums = Album.objects.all().filter(published='PUBLIC')
        if albums.count():
            context = {
                'albums': albums
                }
            return context


class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'imager_images/library.html'
    context_object_name = 'library'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')

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


# class PhotoView(LoginRequiredMixin, DetailView):
#     template_name = 'imager_images/photo.html'
#     pk_url_kwarg = 'photo_id'
#     model = Photo
#     context_object_name = 'single_photo'
#     login_url = reverse_lazy('auth_login')
#     success_url = reverse_lazy('photos')

#     def get(self, *args, **kwargs):
#         """something here"""
#         if not self.request.user.get_username():
#             return redirect('home')
#         self.username = self.request.user.get_username()
#         return super().get(*args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = get_object_or_404(User, username=self.username)
#         albums = (self._public_or_user(Album, self.username))
#         photos = (self._public_or_user(Photo, self.username))
#         context['profile'] = profile
#         context['albums'] = albums
#         context['photos'] = photos
#         context['background'] = sample(list(Photo.objects.filter(published='PUBLIC')) * [None], 1)[0]
#         # if self.kwargs[id]:
#         #     photo_id = self.kwargs[id]
#         #     photo = get_object_or_404(Photo, id=photo_id)
#         #     context = {
#         #         'photo': {'thumb': photo, 'link': reverse('photos')}
#         #         }
#         return context


class PhotoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'imager_images/photo.html'
    model = Photo
    login_url = reverse_lazy('auth_url')
    pk_url_kwarg = 'photo_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, user__username=self.username)
        # albums = (self._public_or_user(Album, self.username))
        # photo = Photo.objects 
        # photos = (self._public_or_user(Photo, self.username))
        # context['profile'] = profile
        # context['albums'] = albums
        # context['photos'] = photos
        # context['background'] = sample(list(Photo.objects.filter(published='PUBLIC')) * [None], 1)[0]
        return context

    def get_queryset(self):
        return Photo.objects.filter(id=self.pk_url_kwarg)


# class ProductCreateView(LoginRequiredMixin, CreateView):
#     template_name = 'store/product_create.html'
#     model = Product
#     form_class = ProductForm
#     success_url = 'store'
#     login_url = reverse_lazy('auth_login')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({'username': self.request.user.username})
#         return kwargs

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class AlbumView(LoginRequiredMixin, DetailView):
#     template_name = 'imager_images/album.html'
#     profile = get_object_or_404(User, username=username)
#     albums = Album.objects.filter(published='PUBLIC')
#     photos = Photo.objects.filter(published='PUBLIC')

#     context = {
#         'profile': profile,
#         'albums': albums,
#         'photos': photos,
#     }
#     if album_id:
#         album = get_object_or_404(Album, id=album_id)
#         context["photos"] = _album_with_cover(Photo.objects.filter(album__id=album.id).filter(published='PUBLIC'), album.cover)
#         context["album"] = album
#         return render(request, 'imager_images/album.html', context)
#     return render(request, 'imager_images/album.html', context)


# def photo_view(request, photo_id=None):
#     username = request.user.get_username()
#     owner = True
#     if username == '':
#         return redirect('home')

#     profile = get_object_or_404(User, username=username)
#     albums = Album.objects.filter(published='PUBLIC')
#     photos = Photo.objects.filter(published='PUBLIC')

#     context = {
#         'profile': profile,
#         'albums': [{'cover': album.cover, 'link': reverse('album',
#                     args=[album.id])} for album in albums],
#         'photos': [{'thumb': photo, 'link': reverse('photos', args=[photo.id])} for photo in photos]
#     }
#     return render(request, 'imager_images/photo.html', context)


def _album_with_cover(photos, cover):
    if cover is not None:
        return set(photos) | {cover}
    return photos


# def album_view(request, album_id=None):
#     """Album View."""
#     username = request.user.get_username()
#     owner = True
#     if username == '':
#         return redirect('home')

#     profile = get_object_or_404(User, username=username)
#     albums = Album.objects.filter(published='PUBLIC')
#     photos = Photo.objects.filter(published='PUBLIC')

#     context = {
#         'profile': profile,
#         'albums': albums,
#         'photos': photos,
#     }
#     if album_id:
#         album = get_object_or_404(Album, id=album_id)
#         context["photos"] = _album_with_cover(Photo.objects.filter(album__id=album.id).filter(published='PUBLIC'), album.cover)
#         context["album"] = album
#         return render(request, 'imager_images/album.html', context)
#     return render(request, 'imager_images/album.html', context)
