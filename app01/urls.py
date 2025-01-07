from django.urls import path,include
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('Player Registration/',views.player_registration,name='player_registration'),
    path('staff Registration/',views.staff_registration,name='staff_registration'),
    path('login/',views.login,name='login'),
    path('landing/',views.landing,name='landing'),
]