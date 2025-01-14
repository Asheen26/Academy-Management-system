from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

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
        registration=player(full_name=full_name,profile_photo=profile_photo,contact=contact,gender=gender,dob=dob,email=email,guardian_name=guardian_name,address=address,jersey_number=jersey_number,position=position,password=password)
        registration.save()
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

