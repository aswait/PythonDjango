from timeit import default_timer

from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .models import Product, Order


def index(request: HttpRequest) -> HttpResponse:
    products = [
        ('laptop', 1999),
        ('desktop', 2999),
        ('smartphone', 999),
    ]

    context = {
        "time_running": default_timer(),
        "products": products
    }
    return render(request, "shoppapp/shop-index.html", context=context)


def groups(request: HttpRequest) -> HttpResponse:
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }

    return render(request, 'shoppapp/groups-list.html', context=context)


def products_list(request: HttpRequest) -> HttpResponse:
    context = {
        "products": Product.objects.all(),
    }

    return render(request, 'shoppapp/products-list.html', context=context)


def orders_list(request: HttpRequest) -> HttpResponse:
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }

    return render(request, 'shoppapp/orders-list.html', context=context)
