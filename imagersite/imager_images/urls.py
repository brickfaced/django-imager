from django.urls import path
from .views import photos_view, albums_view


urlpatterns = [
    path('photos', photos_view, name='photos'),
    path('albums', albums_view, name='albums'),
    # path('photos/<str:title>', photo_view, name='photo'),
    # path('settings/<str:title>', home_view, name='settings')  # The view is not correct here. You need to define settings_view
]