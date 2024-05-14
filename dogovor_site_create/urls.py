from django.urls import path

from dogovor_site_create import views

urlpatterns = [
    path('', views.process_contract, name='process_contract'),  # Используйте '', если path('dogovor_pbn/') уже перенаправляет сюда
]