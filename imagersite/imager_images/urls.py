from django.urls import path
from .views import photos_view, albums_view, library_view, photo_view, album_view


urlpatterns = [
    path('photos', photos_view, name='photos'),
    path('albums', albums_view, name='albums'),
    path('library', library_view, name='library'),
    path('photos/<photo_id>', photo_view, name='single_photo'),
    path('albums/<str:album_id>', album_view, name='album'),
]