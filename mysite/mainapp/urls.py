from django.urls import path
from .views import *


app_name = 'mainapp'

urlpatterns = [
    path('', tour_list, name='tour_list'),
    path('login/',login,name='login'),
    path('registration/',registration,name='registration'),
    path('logout/',logoutUser,name='logout'),
    path('profile/',user_profile,name='profile'),
    path('createtour',create_tour,name='createtour'),
    path('tournament/<int:id>',tour,name="tour"),
]
