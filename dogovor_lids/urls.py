from django.urls import path

from dogovor_lids import views

urlpatterns = [
    path('', views.process_contract, name='process_contract'),
]
