from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/enhance/', views.enhance_api, name='enhance_api'),
]

