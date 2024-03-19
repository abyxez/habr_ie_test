from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient, APITestCase

from comics.models import Comic, Rating

User = get_user_model()


class PostRateTestCase(APITestCase):
    """
    Проверяем существование первичной оценки
    и её обновление
    """

    def setUp(self) -> None:
        self.tester = User.objects.create(
            username="test1",
            email="test1@mail.ru",
            password="password",
        )
        self.author = User.objects.create(
            username="admin",
            email="admin@mail.ru",
            password="admin",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.tester)
        self.comic = Comic.objects.create(title="title", author=self.author)

    def test_rate_created_and_comic_rate_changed(self):
        self.assertEqual(self.comic.rating, 0)

        data = {
            "comic_id": self.comic.id,
            "user_id": self.tester.id,
            "value": 3,
        }
        response = self.client.post(
            reverse("api:ratings-list"), data=data, format="json"
        )

        self.assertTrue(response.status_code, HTTP_200_OK)
        self.assertTrue(
            Rating.objects.filter(
                comic_id=self.comic, user_id=self.tester, value=data["value"]
            ).exists()
        )
        self.assertEqual(
            Comic.objects.get(id=self.comic.id).rating, data["value"]
        )


class CheckAvgRateTestCase(APITestCase):
    """
    Проверяем правильность вычисления Rating avg
    """

    def setUp(self) -> None:
        self.tester1 = User.objects.create(
            username="test1",
            email="test1@mail.ru",
            password="password",
        )
        self.tester2 = User.objects.create(
            username="test2",
            email="test2@mail.ru",
            password="password",
        )
        self.tester3 = User.objects.create(
            username="test3",
            email="test3@mail.ru",
            password="password",
        )
        self.author = User.objects.create(
            username="admin",
            email="admin@mail.ru",
            password="admin",
        )
        self.client1 = APIClient()
        self.client1.force_authenticate(self.tester1)
        self.client2 = APIClient()
        self.client2.force_authenticate(self.tester2)

        self.comic = Comic.objects.create(
            title="title",
            author=self.author,
        )

    def test_rate_created_and_comic_rate_changed(self):
        data1 = {
            "comic_id": self.comic.id,
            "user_id": self.tester1.id,
            "value": 4,
        }
        data2 = {
            "comic_id": self.comic.id,
            "user_id": self.tester2.id,
            "value": 1,
        }
        self.client1.post(
            reverse("api:ratings-list"), data=data1, format="json"
        )
        self.client2.post(
            reverse("api:ratings-list"), data=data2, format="json"
        )

        expected_value = round(
            (data1["value"] + data2["value"]) / len(Rating.objects.all()), 1
        )

        self.assertEqual(
            Comic.objects.get(id=self.comic.id).rating, expected_value
        )
