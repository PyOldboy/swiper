from rest_framework import serializers

from profile.models import Profile


class ASerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['dating_location','dating_gender','min_distance',
                  'max_distance','min_dating_age','max_dating_age',
                  'vibration','only_matched','auto_play']
