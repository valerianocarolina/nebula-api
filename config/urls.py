from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/v1/',
        include('users.urls')
    ),

    path(
        'api/v1/posts/',
        include('posts.urls'),
    ),

    path(
        'api/v1/friendships/',
        include('friendships.urls')
    ),

    path(
        'api/v1/conversations/',
        include('chat.urls'),
    ),

    path(
        'api/v1/',
        include('reports.urls'),
    ),

    path(
        'api/v1/',
        include('administration.urls'),
    ),

    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )