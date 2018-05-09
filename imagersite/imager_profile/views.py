from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from imager_images.models import Photo, Album
from .models import ImagerProfile


class ProfileView(ListView):
    template_name = 'imager_profile/user.html'
    context_object_name = 'profile'

    def get(self, *args, **kwargs):
        if not self.request.user.get_username():
            return redirect('home')
        self.username = self.request.user.get_username()
        
        return super().get(*args, **kwargs)

    def get_queryset(self):
        if self.username:
            profile = get_object_or_404(ImagerProfile, user__username=self.username)
            album = Album.objects.filter(user__username=self.username)
            photos = Photo.objects.filter(album__user__username=self.username)
            context = {'profile': profile, 'album': album, 'photos': photos}

        else:
            photos = Photo.objects.filter(published='PUBLIC')
            album = Album.objects.filter(published='PUBLIC')
            context = {
                'album': album,
                'photos': photos
                }
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context