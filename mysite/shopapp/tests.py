from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from shopapp.models import Product
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self) -> None:
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create(self) -> None:
        c = Client(HTTP_USER_AGENT="Mozilla/5.0")
        response = c.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(
            name="".join(choices(ascii_letters, k=10))
        )
        cls.user_agent = Client(HTTP_USER_AGENT="Mozilla/5.0")

    def test_get_product(self):
        response = self.user_agent.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.user_agent.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'shopapp-fixtures.json',
    ]

    def test_products(self):
        c = Client(HTTP_USER_AGENT="Mozilla/5.0")
        response = c.get(reverse("shopapp:products_list"))
        products = Product.objects.filter(archived=False).all()
        products_ = response.context["products"]

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="".join(choices(ascii_letters, k=10)),
            password="".join(choices(ascii_letters, k=10))
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.c = Client(HTTP_USER_AGENT="Mozilla/5.0")
        self.c.force_login(self.user)

    def test_orders_view(self):
        response = self.c.get(reverse("shopapp:order_list"))
        self.assertContains(response, "Orders")

    def test_order_view_not_authenticated(self):
        self.c.logout()
        response = self.c.get(reverse("shopapp:order_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "shopapp-fixtures.json",
    ]

    def setUp(self) -> None:
        self.c = Client(HTTP_USER_AGENT="Mozilla/5.0")

    def test_get_products_view(self) -> None:
        response = self.c.get(
            reverse("shopapp:products-export")
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )

