from django.contrib import admin

# Register your models here.
from . models import player
from . models import staff
from . models import Attendance

class playeradmin(admin.ModelAdmin):
    list_display=('full_name','profile_photo','contact','gender','dob','email','guardian_name','address','jersey_number','position','password')
admin.site.register(player,playeradmin)

class staffadmin(admin.ModelAdmin):
    list_display=('full_name','profile_photo','contact','gender','dob','email','address','department','role','qualification','password')
admin.site.register(staff,staffadmin)  

class Attendanceadmin(admin.ModelAdmin):
    list_display=('player_dtls', 'date', 'status', 'late_minutes', 'taken_by')
    search_fields = ('player_dtls__full_name', 'status', 'taken_by__full_name', 'date')
    list_filter = ('status', 'date')
admin.site.register(Attendance,Attendanceadmin)    
