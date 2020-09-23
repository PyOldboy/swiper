from django.urls import path

from profile import views

urlpatterns= [
    path('show/',views.ProfileShow.as_view()),

    path('update/', views.ProfileUpdate)
]