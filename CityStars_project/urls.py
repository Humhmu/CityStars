from django.contrib import admin
from django.urls import path, include
from CityStars_app import views

urlpatterns = [
    path("", views.city_stars, name="city_stars"),
    path("city_stars/", include("CityStars_app.urls")),
    path("admin/", admin.site.urls),
]
