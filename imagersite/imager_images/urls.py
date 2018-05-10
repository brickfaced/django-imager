from django.urls import path
from .views import PhotosView, AlbumsView, LibraryView, PhotoDetailView

urlpatterns = [
    path('photos', PhotosView.as_view(), name='photos'),
    path('albums', AlbumsView.as_view(), name='albums'),
    path('library', LibraryView.as_view(), name='library'),
    path('photos/<photo_id>', PhotoDetailView.as_view(), name='single_photo'),
    # path('photos/<photo_id>/edit', PhotoView.as_view(), name='single_photo'),
    # path('albums/<str:album_id>', album_view, name='album'),
]