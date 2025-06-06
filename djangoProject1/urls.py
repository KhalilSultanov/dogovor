from django.contrib import admin
from django.urls import path, include

from selection.login import login

urlpatterns = [
    path('', login, name='login'),

    path('main/', include('selection.urls')),  # Просто подключай app напрямую
    path('main/admin/', admin.site.urls),
    path('main/dogovor_pbn/', include('dogovor_pbn.urls')),
    path('main/dogovor_position/', include('dogovor_position.urls')),
    path('main/dogovor_pf/', include('dogovor_pf.urls')),
    path('main/dogovor_fix/', include('dogovor_fix.urls')),
    path('main/dogovor_traffic/', include('dogovor_traffic.urls')),
    path('main/dogovor_site_create/', include('dogovor_site_create.urls')),
    path('main/dogovor_yandex_direct/', include('dogovor_yandex_direct.urls')),
    path('main/dogovor_lids/', include('dogovor_lids.urls')),
]
