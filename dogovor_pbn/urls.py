from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_contract, name='process_contract'),  # Используйте '', если path('dogovor_pbn/') уже перенаправляет сюда
]