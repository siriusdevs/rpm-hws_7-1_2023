from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as status_codes
from django.shortcuts import render
from . import config
from .models import Places
from . import serializers


def main_page(req):
    return render(
        req,
        config.MAIN_PAGE,
    )


def places(req):
    return render(
        req,
        config.PLACES_PAGE,
        context={
            'places_с': Places.objects.all().count(),
            'places': Places.objects.all(),
        },
    )


def find_place(req):
    points = "58.46970671,51.23065552"
    scale = 13
    if req.GET.get('f_place', ''):
        # Типа штука что бы выдавалась только первое значение без повторений
        f_place = Places.objects.filter(name=req.GET.get('f_place', '')).first()
        if f_place:
            points = f_place.map_points
            scale = f_place.map_scale
    return render(
        req,
        config.FIND_PLACE_PAGE,
        context={
            'places': Places.objects.all(),
            'points': points,
            'scale': scale
        },
    )


def query_from_request(request, cls_serializer=None) -> dict:
    if cls_serializer:
        query = {}
        for attr in cls_serializer.Meta.fields:
            attr_value = request.GET.get(attr, '')
            if attr_value:
                query[attr] = attr_value
        return query
    return request.GET


# Попытка переписать это под адекватный код
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PlacesList(APIView):

    def get_object(self, pk):
        try:
            return Places.objects.get(id=pk)
        except Places.DoesNotExist:
            raise Exception()

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = serializers.PlacesSerializer(place)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.PlacesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status_codes.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = serializers.PlacesSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = self.get_object(pk)
        place.delete()
        return Response(status=status_codes.HTTP_204_NO_CONTENT)
