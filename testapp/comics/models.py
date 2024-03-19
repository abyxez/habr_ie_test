from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()


class Author(models.Model):

    name = models.CharField(_("Автор комикса"), max_length=50)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})


class Comic(models.Model):
    title = models.CharField(
        max_length=200,
    )
    author = models.ForeignKey(
        to=User, verbose_name="Автор", on_delete=models.CASCADE
    )
    rating = models.FloatField(
        default=0,
    )


class Rating(models.Model):

    comic_id = models.ForeignKey(
        "comics.Comic",
        verbose_name=_("Комикс"),
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        to=User,
        verbose_name=_("Пользователь"),
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        verbose_name=_("Оценка"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    def __str__(self):
        return f'{self.comic_id}: {self.user_id}"s rate is {self.value}'

    def get_absolute_url(self):
        return reverse("Rating_detail", kwargs={"pk": self.pk})
