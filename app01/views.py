from django.shortcuts import render
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

def staff_registration(request):
    return render(request,'staff_registration.html')

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
    else:
        return render(request,'index.html',{'status': 'Invalid email or password'})

def landing(request):
    return render(request,'landing.html')