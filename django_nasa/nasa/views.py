"""Some function for nasa entrypoints."""
import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests as req
from django.core.handlers.wsgi import WSGIRequest
from django_nasa.settings import IMAGE_API_TOKEN, IMAGE_API_URL


# Create your views here.

def home_page(request: WSGIRequest):
    """Displays home page.

    Args:
        request (WSGIRequest): request
    """
    return redirect("nasa_page")


def nasa_page(request):
    """Displays nasa page.

    Args:
        request (WSGIRequest): request
    """
    image = {}
    if request.method == 'GET':
        source = request.GET.get('source')
        if source:
            return image_api(source, request.GET)
        try:
            image = req.get(IMAGE_API_URL + f"/image/nasa/?token={IMAGE_API_TOKEN}").json()
        except Exception:
            logging.warning("Image api server is not responding")
    return render(request, "nasa.html",
                  {"image": image})


def mars_page(request: WSGIRequest):
    """Displays home page.

    Args:
        request (WSGIRequest): request
    """
    image = {}
    if request.method == 'GET':
        source = request.GET.get('source')
        if source:
            return image_api(source, request.GET)
        try:
            image = req.get(IMAGE_API_URL + f"/image/mars/?token={IMAGE_API_TOKEN}").json()
        except Exception:
            logging.warning("Image api server is not responding")
    return render(request, "mars.html",
                  {"image": image})


def user_page(request: WSGIRequest):
    """Displays home page.

    Args:
        request (WSGIRequest): request
    """
    if request.method == 'GET':
        source = request.GET.get('source')
        if source:
            return image_api(source, request.GET)

    return render(request, "user.html",
                  {"image": request.GET})


def user_image_page(request: WSGIRequest):
    """Displays home page.

    Args:
        request (WSGIRequest): request
    """
    img_url = ''
    if request.method == 'GET':
        source = request.GET.get('source')
        if source:
            return image_api(source, request.GET)
        img_url = IMAGE_API_URL + f"/image/user{request.GET.get('url')}?token={IMAGE_API_TOKEN}"
    return render(request, "user_image.html",
                  {"image": request.GET, "img_url": img_url})


def image_api(source: str, query: dict) -> JsonResponse:
    """Returns json from image api.

    Args:
        source (str): request source.
        query (dict): parameters for request to image api.
    """
    image = {}
    if source == 'nasa':
        image = req.get(IMAGE_API_URL + f"/image/nasa/{query.get('date')}/?token={IMAGE_API_TOKEN}").json()
    elif source == 'nasa-random':
        image = req.get(IMAGE_API_URL + f"/image/nasa/random/?token={IMAGE_API_TOKEN}").json()
    elif source == "mars":
        image = req.get(IMAGE_API_URL + f"/image/mars/{query.get('date')}/?token={IMAGE_API_TOKEN}").json()
    elif source == "user":
        image = req.get(IMAGE_API_URL + f"/image/user/{query.get('username')}/?token={IMAGE_API_TOKEN}").json()
    return JsonResponse(image, safe=False)
