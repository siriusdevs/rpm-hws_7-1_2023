from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test.client import Client
from places_app.models import Places
from rest_framework import status
from rest_framework.test import APIClient

url = "/places/"
url2 = "/update_place/"
content_post = {
    "name": "Щаааурмечная",
    "description": "Лучшая шаурма в Сириусе",
    "map_points": "39.95696487,43.41423849",
    "map_scale": 17
}
content_put = {
    'name': 'shaurmechnaya',
    'map_scale': 15
}


class ViewSetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.creds_user = {'username': 'user', 'password': 'user'}
        self.creds_superuser = {'username': 'superuser', 'password': 'superuser'}
        self.user = User.objects.create_user(**self.creds_user)
        self.superuser = User.objects.create_user(is_superuser=True, **self.creds_superuser)
        self.token = Token.objects.create(user=self.superuser)

    def test_get(self):
        # logging in with user
        self.client.login(**self.creds_user)
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, status.HTTP_200_OK)

        # logging out
        self.client.logout()

    def test_manage(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser, token=self.token)
        # POST
        resp_post = self.client.post(url2, data=content_post)
        self.assertEqual(resp_post.status_code, status.HTTP_201_CREATED)

        # PUT
        created = Places.objects.get(**content_post)
        url_to_created = f'{url2}{created.id}'
        resp_put = self.client.put(url_to_created, data=content_put)
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)

        # DELETE EXISTING
        resp_delete = self.client.delete(url_to_created)
        self.assertEqual(resp_delete.status_code, status.HTTP_204_NO_CONTENT)

        # DELETE NONEXISTENT
        resp_delete = self.client.delete(url_to_created)
        self.assertEqual(resp_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_manage_token(self):
        # logging in with rest_framework APIClient
        # (it can be forcefully authenticated with token)
        self.client = APIClient()

        # token goes brrr
        self.client.force_authenticate(user=self.superuser, token=self.token)
