from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth import get_user_model

from comics.models import Comic, Rating

EMPTY_VALUE_DISPLAY = "-empty-"
site.site_header = "Admin panel"


User = get_user_model()


@register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = (
        "id",
        "comic_id",
        "user_id",
        "value",
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Comic)
class ComicAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "rating",
    )
    search_fields = ("name",)
    empty_value_display = EMPTY_VALUE_DISPLAY
