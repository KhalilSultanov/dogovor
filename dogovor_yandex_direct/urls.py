from django.urls import path

from dogovor_yandex_direct import views

urlpatterns = [
    path('', views.process_contract, name='process_contract'),
]
