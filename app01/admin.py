from django.contrib import admin

# Register your models here.
from . models import player
from . models import staff

class playeradmin(admin.ModelAdmin):
    list_display=('full_name','profile_photo','contact','gender','dob','email','guardian_name','address','jersey_number','position','password')
admin.site.register(player,playeradmin)

class staffadmin(admin.ModelAdmin):
    list_display=('full_name','profile_photo','contact','gender','dob','email','address','department','role','qualification','password')
admin.site.register(staff,staffadmin)    
