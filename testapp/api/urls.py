from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ComicViewSet, RatingViewSet

app_name = "api"

router = DefaultRouter()

router.register(r"comics", ComicViewSet, "comics")
router.register("ratings", RatingViewSet, "ratings")

urlpatterns = [
    path("", include(router.urls)),
]
