from django.contrib import admin
from django.urls import path, include

from selection.login import login

urlpatterns = [
    path('', login, name='login'),  # Обработчик для стартовой страницы
    path('main/', include([
        path('', include('selection.urls')),  # URL для начальной страницы теперь будет /main/
        path('admin/', admin.site.urls),  # URL для админки теперь будет /main/admin/
        path('dogovor_pbn/', include('dogovor_pbn.urls')),  # и так далее для остальных приложений
        path('dogovor_position/', include('dogovor_position.urls')),
        path('dogovor_pf/', include('dogovor_pf.urls')),
        path('dogovor_fix/', include('dogovor_fix.urls')),
        path('dogovor_traffic/', include('dogovor_traffic.urls')),
        path('dogovor_site_create/', include('dogovor_site_create.urls')),
    ])),
]
