from django.db import models

# Create your models here.

class player(models.Model):
    full_name=models.CharField(max_length=200)
    profile_photo=models.ImageField(upload_to='plyrprof')
    contact=models.CharField(max_length=200)
    gender=models.CharField(max_length=200)
    dob=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    guardian_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    jersey_number=models.CharField(max_length=200)
    position=models.CharField(max_length=200)
    password=models.CharField(max_length=200)

    def __str__(self):
        return self.full_name    

class staff(models.Model):
    full_name=models.CharField(max_length=200)
    profile_photo=models.ImageField(upload_to='plyrprof')
    contact=models.CharField(max_length=200)
    gender=models.CharField(max_length=200)
    dob=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    role=models.CharField(max_length=200)
    qualification=models.CharField(max_length=200)
    password=models.CharField(max_length=200)

    def __str__(self):
        return self.full_name    

   
# Attendance model
class Attendance(models.Model):

    player_dtls = models.ForeignKey(player, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Present')
    late_minutes = models.PositiveIntegerField(null=True, blank=True)  # Optional field for late minutes
    taken_by = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, related_name='attendances_taken')

    def __str__(self):
        return f"{self.player_dtls.full_name} - {self.date} - {self.status}"

