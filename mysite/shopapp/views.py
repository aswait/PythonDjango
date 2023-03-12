from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


# Create your views here.


def shop_index(request: HttpRequest):
    products = [
        ('laptop', 1999),
        ('desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running":  default_timer(),
        "products": products
    }
    return render(request, 'shopapp/shop-index.html', context=context)
