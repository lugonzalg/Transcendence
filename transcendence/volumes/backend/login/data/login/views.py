from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

import logging

logger = logging.getLogger(__name__)

def handle_post():
    logger.warning(1)
    return {"user": "jimmy"}

def handle_get():
    logger.warning(2)
    return {"user": "lukas"}

method = {
    'POST': handle_post,
    'GET': handle_post
}

# Create your views here.
@csrf_exempt
def create_user(request: HttpRequest) -> HttpResponse:

    callback = method.get(request.method)
    if callback is None:
        raise Http404("Error: Not found")

    return callback(request)