from django.shortcuts import render


def home_view(request):
    return render(request, 'generic/home.html', {'message': 'Hey this is our website', 
                                                    'image': 'http://via.placeholder.com/350x300'})
