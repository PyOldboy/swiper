from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from profile.serializers import ASerializer

# Create your views here.
from profile.models import Profile


class ProfileShow(View):
    def get(self,request):
        profile_list = Profile.objects.all()

        profile_serializer = ASerializer(profile_list,many=True)

        data = {
            'code': 0,
            'animal': profile_serializer.data
        }
        return JsonResponse(data=data)


def ProfileUpdate(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        dating_gender = request.POST.get('dating_gender')
        dating_location = request.POST.get('dating_location')
        max_distance = request.POST.get('max_distance')
        min_distance = request.POST.get('min_distance')
        max_dating_age = request.POST.get('max_dating_age')
        min_dating_age = request.POST.get('min_dating_age')
        vibration = request.POST.get('vibration')
        only_matched = request.POST.get('only_matched')
        auto_play = request.POST.get('auto_play')

        data ={}
        return JsonResponse(data=data)