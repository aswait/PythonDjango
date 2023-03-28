from typing import Callable

from django.http import HttpRequest, HttpResponse
from types import FunctionType


def setup_useragent_on_request_middleware(get_response) -> Callable[[HttpRequest], HttpResponse]:

    print("initial call")

    def middleware(request: HttpRequest) -> HttpResponse:

        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")

        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("response count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")

