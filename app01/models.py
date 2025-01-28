from django.db import models
from django.utils.timezone import now

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


class Stats(models.Model):
    player_dtls = models.ForeignKey(player, on_delete=models.CASCADE, related_name='stats_records')
    matches=models.CharField(max_length=10)
    goals=models.CharField(max_length=10)
    assists=models.CharField(max_length=10)
    saves=models.CharField(max_length=10)
    tackles=models.CharField(max_length=10)
    given_by=models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, related_name='stats_given')
    
    def __str__(self):
        return f"{self.player_dtls.full_name}"





class Message(models.Model):
    sender = models.ForeignKey('staff', on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    receiver_department = models.CharField(max_length=255, null=True, blank=True)  # For department messages
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.full_name if self.sender else 'Admin'} to {self.receiver_department or 'Players'}"




class Workload(models.Model):
    player = models.ForeignKey(player, on_delete=models.CASCADE)
    training_minutes = models.IntegerField(default=0)
    intensity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    match_minutes = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)  # Distance in kilometers
    
    # Calculated values (workload only)
    training_workload = models.CharField(max_length=10,default='low')
    match_workload = models.CharField(max_length=10,default='low')
    total_workload = models.CharField(max_length=10,default='low')
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Workload for {self.player.full_name} ({self.last_updated})"



class TrainingSession(models.Model):
    SESSION_CHOICES = [
        ('Session 1', 'Session 1'),
        ('Session 2', 'Session 2'),
        ('Session 3', 'Session 3'),
    ]

    session_name = models.CharField(max_length=20, choices=SESSION_CHOICES)
    monday = models.CharField(max_length=50, default='Rest')
    tuesday = models.CharField(max_length=50, default='Rest')
    wednesday = models.CharField(max_length=50, default='Rest')
    thursday = models.CharField(max_length=50, default='Rest')
    friday = models.CharField(max_length=50, default='Rest')
    saturday = models.CharField(max_length=50, default='Rest')
    sunday = models.CharField(max_length=50, default='Rest')

    def __str__(self):
        return self.session_name



class InjuryList(models.Model):
    player_injured = models.ForeignKey(player, on_delete=models.CASCADE)
    injury_type=models.CharField(max_length=200)
    injury_date=models.DateField()
    out_for=models.CharField(max_length=100)
    recovery_programme=models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)  
    
    def __str__(self):
        return f"{self.player_injured.full_name} - {self.injury_type}"
 

