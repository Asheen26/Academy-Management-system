from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from datetime import date

from . models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def player_registration(request):
    if request.method=="POST":
        full_name=request.POST.get('full_name')
        profile_photo=request.FILES.get('profile_photo')
        f=FileSystemStorage()
        fs=f.save(profile_photo.name,profile_photo)
        contact=request.POST.get('contact')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        guardian_name=request.POST.get('guardian_name')
        address=request.POST.get('address')
        jersey_number=request.POST.get('jersey_number')
        position=request.POST.get('position')
        password=request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'player_registration.html', {'error_message': 'Passwords do not match.'})


        registration=player(full_name=full_name,profile_photo=profile_photo,contact=contact,gender=gender,dob=dob,email=email,guardian_name=guardian_name,address=address,jersey_number=jersey_number,position=position,password=password)
        registration.save()
        messages.success(request, "Player successfully registered!")
        return redirect('player_registration')
    return render(request,'player_registration.html')



def login(request):
    email=request.POST.get('email')
    password=request.POST.get('password')

    if player.objects.filter(email=email,password=password).exists():
        playerdetls=player.objects.get(email=email,password=password)
        if playerdetls.password==request.POST['password']:
            request.session['pid']=playerdetls.id
            request.session['pname']=playerdetls.full_name
            request.session['email']=playerdetls.email
            request.session['puser']='puser'

            return render(request,'landing.html')
        
    elif staff.objects.filter(email=email,password=password).exists():
        staffdetls=staff.objects.get(email=email,password=password)
        if staffdetls.password==request.POST['password']:
            request.session['sid']=staffdetls.id
            request.session['sname']=staffdetls.full_name
            request.session['email']=staffdetls.email
            request.session['department']=staffdetls.department
            request.session['suser']='suser'

            if staffdetls.department=='Admin':
                return redirect('admin_dashboard')
            elif staffdetls.department=='Coach':
                return redirect('coach_dashboard')
            elif staffdetls.department=='Medical':
                return redirect('medical_dashboard')
            else:
                staffdetls.department=='Analyst'
                return redirect('analyst_dashboard')

              
    else:
        return render(request,'index.html',{'status': 'Invalid email or password'})

def landing(request):
    return render(request,'landing.html')

def player_profile(request):
    tem=request.session['pid']
    vpro=player.objects.get(id=tem)
    return render(request,'player_profile.html',{'result':vpro})

def logout(request):
    session_keys= list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(index)




def staff_registration(request):
    if request.method=="POST":
        full_name=request.POST.get('full_name')
        profile_photo=request.FILES.get('profile_photo')
        f=FileSystemStorage()
        fs=f.save(profile_photo.name,profile_photo)
        contact=request.POST.get('contact')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        address=request.POST.get('address')
        department=request.POST.get('department')
        role=request.POST.get('role')
        qualification=request.POST.get('qualification')
        password=request.POST.get('password')
        registration=staff(full_name=full_name,profile_photo=profile_photo,contact=contact,gender=gender,dob=dob,email=email,address=address,department=department,role=role,qualification=qualification,password=password)
        registration.save()
    return render(request,'staff_registration.html')


    

def staff_landing(request):
    return render(request,'staff_landing.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def coach_dashboard(request):
    return render(request,'coach_dashboard.html')

def medical_dashboard(request):
    return render(request,'medical_dashboard.html')

def analyst_dashboard(request):
    return render(request,'analyst_dashboard.html')




def take_player_attendance(request):
    if request.method == "POST":
        attendance_date = request.POST.get('attendance_date', date.today())
        for player_instance in player.objects.all():
            # Get the attendance status using the player ID
            attendance_status = request.POST.get(f'attendance_{player_instance.id}')
            late_minutes = request.POST.get(f'late_minutes_{player_instance.id}', None)

            # Skip if no attendance status is selected for the player
            if not attendance_status:
                continue

            # Convert late_minutes to an integer if it's not empty and "Late" is selected
            if attendance_status == "Late" and late_minutes:
                late_minutes = int(late_minutes)
            else:
                late_minutes = None

            # Save attendance record
            Attendance.objects.create(
                player_dtls=player_instance,
                date=attendance_date,
                status=attendance_status,
                late_minutes=late_minutes,
                taken_by=staff.objects.get(id=request.session['sid']),  # Assuming staff is logged in
            )

        messages.success(request, "Attendance successfully saved!")
        return redirect('coach_dashboard')
    today_date = date.today()
    players = player.objects.all()
    return render(request, 'take_player_attendance.html', {'players': players, 'today_date': today_date})




def view_player_attendance(request):
    if request.method == "GET":
        # Get the date from the query parameters
        filter_date = request.GET.get('filter_date')
        
        if filter_date:
            # Filter attendance records by the selected date
            attendance_records = Attendance.objects.filter(date=filter_date).select_related('player_dtls')
        else:
            # Show all records if no date is selected
            attendance_records = Attendance.objects.all().select_related('player_dtls')

        context = {
            'attendance_records': attendance_records,
            'filter_date': filter_date,  # To prefill the date field in the template
        }
        return render(request, 'view_player_attendance.html', context)

