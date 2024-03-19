from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from comics.models import Comic, Rating

User = get_user_model()


class ComicSerializer(ModelSerializer):
    ratings = SerializerMethodField()

    class Meta:
        model = Comic
        fields = ("id", "title", "author", "ratings")
        read_only_fields = ("__all__",)

    def get_ratings(self, obj):
        return Rating.objects.filter(comic_id=obj.id).count()


class ComicDetailSerializer(ComicSerializer):
    rating = SerializerMethodField()

    class Meta:  # type: ignore
        model = Comic
        fields = ("rating",)
        read_only_fields = ("__all__",)

    def get_rating(self, obj):
        if not Rating.objects.filter(comic_id=obj).exists():
            return obj.rating

        return round(
            Rating.objects.all()
            .filter(comic_id=obj)
            .aggregate(rating=Avg("value"))["rating"],
            1,
        )


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "id",
            "comic_id",
            "user_id",
            "value",
        )
        read_only_fields = ("__all__",)

    def create(self, validated_data):
        request_user = self.context["request"].user
        user_id = validated_data.get("user_id")

        if request_user != user_id:
            raise ValidationError(
                "Нельзя поставить или поменять оценку другого пользователя!"
            )

        comic_obj = validated_data.get("comic_id")
        value = validated_data.get("value")

        if Rating.objects.filter(comic_id=comic_obj, user_id=user_id).exists():
            rating = Rating.objects.get(comic_id=comic_obj, user_id=user_id)
            rating.value = value
            rating.save()
            return rating

        rating = Rating.objects.create(**validated_data)

        comic = Comic.objects.get(id=comic_obj.id)
        new_comic_rating = round(
            Rating.objects.filter(comic_id=comic_obj).aggregate(
                rating=Avg("value")
            )["rating"],
            1,
        )
        comic.rating = new_comic_rating
        comic.save()

        return rating
