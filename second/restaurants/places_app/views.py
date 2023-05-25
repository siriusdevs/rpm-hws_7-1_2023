from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
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


# Попытка переписать это под адекватный код
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PlacesList(APIView):

    def get_object(self, p_id):
        try:
            return Places.objects.get(id=p_id)
        except Places.DoesNotExist:
            return None

    def get(self, request, p_id=None):
        if p_id:
            place = self.get_object(p_id)
        else:
            place = Places.objects.filter(**request.data).first()
        if not place:
            return Response("Such a place does not exist", status=status_codes.HTTP_404_NOT_FOUND)
        serializer = serializers.PlacesSerializer(place)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PlacesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status_codes.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def put(self, request, p_id):
        if p_id:
            place = self.get_object(p_id)
        else:
            place = Places.objects.filter(**request.data).first()
        if not place:
            return Response("Such a place does not exist", status=status_codes.HTTP_404_NOT_FOUND)
        serializer = serializers.PlacesSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def delete(self, request, p_id):
        if p_id:
            place = self.get_object(p_id)
        else:
            place = Places.objects.filter(**request.data).first()
        if not place:
            return Response("Such a place does not exist", status=status_codes.HTTP_404_NOT_FOUND)
        place.delete()
        return Response(status=status_codes.HTTP_204_NO_CONTENT)
