from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('ayuda/',views.ayuda,name = 'ayuda'),
    path('home/',views.home,name = 'home'),
    path('peticiones/',views.peticiones,name='peticiones'),
    path('index/',views.add,name = 'index'),
]