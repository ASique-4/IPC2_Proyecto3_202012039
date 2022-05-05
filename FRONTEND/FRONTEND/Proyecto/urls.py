from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.add,name = 'index'),
    path('peticiones/',views.peticiones,name='peticiones'),
    path('index/',views.add,name = 'index'),
]