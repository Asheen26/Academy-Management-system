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

   


