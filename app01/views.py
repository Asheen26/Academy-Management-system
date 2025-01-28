from django.shortcuts import render,redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages 
from django.contrib import messages as django_messages
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

            return redirect('landing')
        
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
        print(request.POST) 
        attendance_date = request.POST.get('attendance_date', date.today())
        for player_instance in player.objects.all():
          
            attendance_status = request.POST.get(f'attendance_{player_instance.id}')
            late_minutes = request.POST.get(f'late_minutes_{player_instance.id}', None)

           
            if not attendance_status:
                continue

          
            if attendance_status == "Late" and late_minutes:
                late_minutes = int(late_minutes)
            else:
                late_minutes = None

       
            Attendance.objects.create(
                player_dtls=player_instance,
                date=attendance_date,
                status=attendance_status,
                late_minutes=late_minutes,
                taken_by=staff.objects.get(id=request.session['sid']),  
            )

        messages.success(request, "Attendance successfully saved!")
        return redirect('coach_dashboard')
    today_date = date.today()
    players = player.objects.all()
    return render(request, 'take_player_attendance.html', {'players': players, 'today_date': today_date})




def view_player_attendance(request):
    if request.method == "GET":
    
        filter_date = request.GET.get('filter_date')
        
        if filter_date:
            
            attendance_records  = Attendance.objects.filter(date=filter_date).select_related('player_dtls')
        else:
           
            attendance_records = Attendance.objects.all().select_related('player_dtls')

        context = {
            'attendance_records': attendance_records,
            'filter_date': filter_date,  
        }
        return render(request, 'view_player_attendance.html', context)



def give_player_stats(request):
    if request.method == 'POST':
        for player_instance in player.objects.all():
            match_stat = request.POST.get(f"matches_{player_instance.id}",0)
            goal_stat = request.POST.get(f"goals_{player_instance.id}",0)
            assist_stat = request.POST.get(f"assists_{player_instance.id}",0)
            tackle_stat = request.POST.get(f"tackles_{player_instance.id}",0)
            save_stat = request.POST.get(f"saves_{player_instance.id}",0)

            
            Stats.objects.update_or_create(
                player_dtls=player_instance,
                defaults={
                    'matches': match_stat,
                    'goals': goal_stat,
                    'assists': assist_stat,
                    'tackles': tackle_stat,
                    'saves': save_stat,
                    'given_by': staff.objects.get(id=request.session['sid']),
                }
            )
        
        messages.success(request, "Player stats successfully updated!")
        return redirect('analyst_dashboard')
    
    
    players = player.objects.all()
    stats = Stats.objects.all()

    return render(request, 'give_player_stats.html', {'players': players, 'stats': stats})

    
    

def view_player_stats(request):

  
    stats = Stats.objects.select_related('player_dtls', 'given_by')  
    return render(request, 'view_player_stats.html', {'stats': stats})





def send_message(request):
    if request.method == "POST":
        sender = staff.objects.get(id=request.session['sid'])  
        recipient_type = request.POST.get('recipient_type')
        content = request.POST.get('content')

        if recipient_type == 'all_players':
            
            Message.objects.create(sender=sender, content=content)
        elif recipient_type in ['Admin', 'Coach', 'Medical', 'Analyst']:
           
            Message.objects.create(sender=sender, receiver_department=recipient_type, content=content)
        
        django_messages.success(request, "Message sent successfully!")
        return redirect('send_message')

    return render(request, 'send_message.html')




def inbox(request):
    user_type = request.session.get('puser') or request.session.get('suser')

    if user_type == 'puser':
        
        messages = Message.objects.filter(receiver_department=None).order_by('-timestamp')
    elif user_type == 'suser':
      
        staff_department = request.session.get('department')
        messages = Message.objects.filter(receiver_department=staff_department).order_by('-timestamp')
    else:
        messages = []

    
    messages.update(is_read=True)

    return render(request, 'inbox.html', {'messages': messages})








def upload_workload(request):
    players = player.objects.all()  
    player_workload_data = []

    if request.method == "POST":
        for player_instance in players:
           
               
            training_minutes = int(request.POST.get(f'training_minutes_{player_instance.id}', 0))
            intensity = request.POST.get(f'intensity_{player_instance.id}', 'low')
            match_minutes = int(request.POST.get(f'match_minutes_{player_instance.id}', 0))
            match_distance = float(request.POST.get(f'distance_{player_instance.id}', 0.0))

              
            training_workload_category, match_workload_category, total_workload_category = calculate_workload(
                    training_minutes, match_minutes, intensity, match_distance)

                
            Workload.objects.update_or_create(
                player=player_instance,
                    defaults={
                        'training_minutes': training_minutes,
                        'intensity': intensity,
                        'match_minutes': match_minutes,
                        'distance': match_distance,
                        'training_workload': training_workload_category,
                        'match_workload': match_workload_category,
                        'total_workload': total_workload_category,
                    }
                )

           


    for player_instance in players:
        workload = Workload.objects.filter(player=player_instance).first()

        
        player_workload_data.append({
            'player': player_instance,
            'training_minutes': workload.training_minutes if workload else 0,
            'intensity': workload.intensity if workload else 'low',
            'match_minutes': workload.match_minutes if workload else 0,
            'distance': workload.distance if workload else 0.0,
            'training_workload': workload.training_workload if workload else 'N/A',
            'match_workload': workload.match_workload if workload else 'N/A',
            'total_workload': workload.total_workload if workload else 'N/A',
        })

 
    return render(request, 'upload_workload.html', {'player_workload_data': player_workload_data})


def calculate_workload(training_minutes, match_minutes, intensity, distance):
  
    if intensity == 'low':
        training_workload = training_minutes * 0.5  
    elif intensity == 'medium':
        training_workload = training_minutes * 1.0  
    elif intensity == 'high':
        training_workload = training_minutes * 1.5  


    match_workload = match_minutes * (1 + distance * 0.2)  
    
 
    if training_workload < 60:
        training_workload_category = 'low'
    elif 60 <= training_workload < 120:
        training_workload_category = 'medium'
    elif 120 <= training_workload < 180:
        training_workload_category = 'high'
    else:
        training_workload_category = 'very high'

    if match_workload < 60:
        match_workload_category = 'low'
    elif 60 <= match_workload < 120:
        match_workload_category = 'medium'
    elif 120 <= match_workload < 180:
        match_workload_category = 'high'
    else:
        match_workload_category = 'very high'
    
    total_workload = (training_workload + match_workload) / 2
    
  
    if total_workload < 60:
        total_workload_category = 'low'
    elif 60 <= total_workload < 120:
        total_workload_category = 'medium'
    elif 120 <= total_workload < 180:
        total_workload_category = 'high'
    else:
        total_workload_category = 'very high'

    return (training_workload_category,match_workload_category,total_workload_category,)


def view_workload(request):

    workloads = Workload.objects.all()  
    return render(request, 'view_workload.html', {'workloads': workloads})





def training_schedule(request):
    categories = [
        "Overall", "Outfield", "Attacking", "Defending", "Possession",
        "Goalkeeping", "Tactical", "Technical", "Set Piece",
        "Match Practice", "Match Preparation", "Physical",
        "Recovery", "Rest", "Match Day", "Extracurricular"
    ]

    if request.method == 'POST':
        for session_index in range(1, 4):  
            session_name = f'Session {session_index}'
            session, created = TrainingSession.objects.get_or_create(session_name=session_name)
            session.monday = request.POST.get(f'session_{session_index}_monday', 'Rest')
            session.tuesday = request.POST.get(f'session_{session_index}_tuesday', 'Rest')
            session.wednesday = request.POST.get(f'session_{session_index}_wednesday', 'Rest')
            session.thursday = request.POST.get(f'session_{session_index}_thursday', 'Rest')
            session.friday = request.POST.get(f'session_{session_index}_friday', 'Rest')
            session.saturday = request.POST.get(f'session_{session_index}_saturday', 'Rest')
            session.sunday = request.POST.get(f'session_{session_index}_sunday', 'Rest')
            session.save()

        return redirect('view_schedule')  

    return render(request, 'training_schedule.html', {
        'categories': categories,
    })

def view_schedule(request):
    sessions = TrainingSession.objects.all()
    return render(request, 'view_schedule.html', {'sessions': sessions})

    

def injury_management(request):
    if request.method == 'POST':
        player_injured = request.POST.get('player_injured')
        injury_type = request.POST.get('injury_type')
        injury_date = request.POST.get('injury_date')
        out_for = request.POST.get('out_for')
        recovery_programme = request.POST.get('recovery_programme', '')

        InjuryList.objects.update_or_create(
            player_injured_id=player_injured,
            injury_type=injury_type,
            injury_date=injury_date,
            out_for=out_for,
            defaults={'recovery_programme': recovery_programme, 'is_active': True}
        )

        return redirect('injury_management')  
    players = player.objects.all()
    active_injuries = InjuryList.objects.filter(is_active=True)

    return render(request, 'injury_management.html', {
        'players': players,
        'active_injuries': active_injuries,})   


def remove_injury(request, id):
    injury = get_object_or_404(InjuryList, id=id)
    injury.is_active = False
    injury.save()
    return redirect('injury_history') 



def active_injury_list(request):
    active_injuries = InjuryList.objects.filter(is_active=True)
    return render(request, 'active_injury_list.html', {
        'active_injuries': active_injuries,})


def injury_history(request):
    injury_history = InjuryList.objects.all()  
    return render(request, 'injury_history.html', {
        'injury_history': injury_history,})


def player_list(request):
    players = player.objects.all()
    return render(request, 'player_list.html', {'players': players})


def list_player_profile(request,id):
    xpro = player.objects.get(id=id)  
    stat = Stats.objects.filter(player_dtls=xpro).first()  
    work = Workload.objects.filter(player=xpro).first()  
    active_injury = InjuryList.objects.filter(player_injured=xpro, is_active=True).first()  

    return render(request, 'list_player_profile.html', {'result':xpro, 'stat':stat, 'work':work, 'active_injury':active_injury,})




def staff_profile(request):
    tem=request.session['sid']
    vpro=staff.objects.get(id=tem)
    return render(request,'staff_profile.html',{'result':vpro})

    
def list_staff_profile(request,id):
    vpro=staff.objects.get(id=id)
    return render(request,'list_staff_profile.html',{'result':vpro})



def staff_list(request):
    staffs = staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})

