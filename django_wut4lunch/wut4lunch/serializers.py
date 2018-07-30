from rest_framework import serializers
from wut4lunch.models import Lunch

class LunchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lunch
        fields = ('submitter', 'food')        