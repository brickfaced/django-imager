from django.views.generic import TemplateView
from imager_images.models import Photo


class HomeView(TemplateView):
    template_name = 'generic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = Photo.objects.all().filter(published='PUBLIC')
        if photos.count():
            context = {'photos': photos}
            return context


