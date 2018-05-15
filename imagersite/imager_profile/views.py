from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView
from imager_images.models import Photo, Album
from .models import ImagerProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProfileEditForm
from random import sample


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'imager_profile/user.html'
    context_object_name = 'profile'
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(ImagerProfile, user__username=self.username)
        albums = Album.objects.filter(user__username=self.username)
        photos = Photo.objects.filter(album__user__username=self.username)

        context['profile'] = profile
        context['albums'] = albums
        context['photos'] = photos
        context['background'] = sample(list(Photo.objects.filter(published="PUBLIC")) + [None], 1)[0]

        return context
    
    def get(self, request, *args, username=None, **kwargs):
        """Get function."""
        username = request.user.get_username()
        if not username:
            return redirect('home')
        self.username = username
        return super().get(request, *args, username=username, **kwargs)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'imager_profile/profile_edit.html'
    model = ImagerProfile
    form_class = ProfileEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.get_username()})
        return kwargs

    def form_valid(self, form):
        form.instance.user.email = form.data['email']
        form.instance.user.first_name = form.data['first_name']
        form.instance.user.last_name = form.data['last_name']
        form.instance.user.save()
        return super().form_valid(form)