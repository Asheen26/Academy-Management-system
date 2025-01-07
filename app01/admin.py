from django.contrib import admin

# Register your models here.
from . models import player

class playeradmin(admin.ModelAdmin):
    list_display=('full_name','profile_photo','contact','gender','dob','email','guardian_name','address','jersey_number','position','password')
admin.site.register(player,playeradmin)
