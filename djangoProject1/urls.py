from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('selection.urls')),  # Предполагаем, что у вас есть приложение selection для начальной страницы
    path('dogovor_pbn/', include('dogovor_pbn.urls')),  # Пути для приложения dogovor_pbn
    path('dogovor_position/', include('dogovor_position.urls')),  # Пути для приложения dogovor_pbn
    path('dogovor_pf/', include('dogovor_pf.urls')),  # Пути для приложения dogovor_pbn
    path('dogovor_fix/', include('dogovor_fix.urls')),  # Пути для приложения dogovor_pbn
    path('dogovor_traffic/', include('dogovor_traffic.urls')),  # Пути для приложения dogovor_pbn
    path('dogovor_site_create/', include('dogovor_site_create.urls')),  # Пути для приложения dogovor_pbn
]
