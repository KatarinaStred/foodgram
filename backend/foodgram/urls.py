from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import get_short_link

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('s/<int:pk>/', get_short_link, name='get_short_link'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
