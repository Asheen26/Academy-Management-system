from django.urls import path,include
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('Player Registration/',views.player_registration,name='player_registration'),
    path('staff Registration/',views.staff_registration,name='staff_registration'),
    path('login/',views.login,name='login'),
    path('landing/',views.landing,name='landing'),
    path('player_profile/',views.player_profile,name='player_profile'),
    path('logout/',views.logout,name='logout'),
    path('staff_landing/',views.staff_landing,name='staff_landing'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('coach_dashboard/',views.coach_dashboard,name='coach_dashboard'),
    path('medical_dashboard/',views.medical_dashboard,name='medical_dashboard'),
    path('analyst_dashboard/',views.analyst_dashboard,name='analyst_dashboard'),
    path('take_player_attendance/',views.take_player_attendance,name='take_player_attendance'),
    path('view_player_attendance/', views.view_player_attendance, name='view_player_attendance'),

]