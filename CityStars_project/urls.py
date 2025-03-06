from django.contrib import admin
from django.urls import path, include
from CityStars_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.city_stars, name="city_stars"),
    path("city_stars/", include("CityStars_app.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
