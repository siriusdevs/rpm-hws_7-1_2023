from .models import Places
from rest_framework.serializers import HyperlinkedModelSerializer


class PlacesSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Places
        fields = ('id', 'name', 'description', 'map_points', 'map_scale')
