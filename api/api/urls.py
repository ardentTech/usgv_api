from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers

from crime.views import GVAIncidentViewSet, GVAStats
from geo.views import UsStateViewSet


router = routers.DefaultRouter()
router.register(r"gva-incident", GVAIncidentViewSet, base_name="gva-incident")
router.register(r"us-state", UsStateViewSet, base_name="us-state")

urlpatterns = [
    url(r"^v1/", include(router.urls, namespace="api")),
    # @todo integrate with default router
    url(r"^v1/gva-stats/", GVAStats.as_view(), name="gva-stats"),
    url(r"^grappelli/", include("grappelli.urls")),
    url(r"^admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
