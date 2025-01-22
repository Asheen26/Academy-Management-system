from django.contrib import admin

# Register your models here.
from . models import player
from . models import staff
from . models import Attendance
from . models import Message
from . models import Workload
from . models import TrainingSession

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

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver_department', 'content', 'timestamp', 'is_read')
    list_filter = ('receiver_department', 'is_read', 'timestamp')
    search_fields = ('sender__full_name', 'content')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
admin.site.register(Message,MessageAdmin)    


class WorkloadAdmin(admin.ModelAdmin):
    list_display=('player','training_minutes','intensity','match_minutes','distance','training_workload','match_workload','total_workload','last_updated')

admin.site.register(Workload,WorkloadAdmin)
    

class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
  

# Register the model with the admin site
admin.site.register(TrainingSession, TrainingSessionAdmin)