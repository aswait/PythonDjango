import json

from django.test import TestCase, Client
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self) -> None:
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get(reverse("myauth:cookie-get"))
        self.assertContains(response, "Cookie value")


class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get(reverse("myauth:foo-bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], "application/json",
        )
        excepted_data = {"foo": "bar", "spam": "eggs"}
        self.assertJSONEqual(response.content, excepted_data)
