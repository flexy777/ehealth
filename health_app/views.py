from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, MedicalInfoForm, MedicalRecordFilterForm, AppointmentForm, AppointmentDecisionForm
from.models import MedicalRecord, UserProfile, CustomUser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.email
            user.save()
            user_type = form.cleaned_data.get('user_type')
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.user_type = user_type
            user_profile.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')   

def user_profile(request):
    medical_record, created = MedicalRecord.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = MedicalInfoForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            return redirect('statistics')

    else:
        form = MedicalInfoForm(instance=medical_record)

    return render(request, 'user_profile.html', {'form': form, 'medical_record': medical_record})

def statistics_view(request):
    medical_records = MedicalRecord.objects.all()
    df = pd.DataFrame(medical_records.values('blood_group'))
    df2 = pd.DataFrame(medical_records.values('genotype'))

    blood_group_counts = df['blood_group'].value_counts()
    blood_group_counts.plot(kind='bar')
    plt.title('Distribution of Blood Groups')
    plt.xlabel('Blood Group')
    plt.ylabel('Count')

    chart_path = 'static/chart.png'
    plt.savefig(chart_path)

    genotype_counts = df2['genotype'].value_counts()
    genotype_counts.plot(kind='bar')
    plt.title('Distribution of Genotype')
    plt.xlabel('Genotype')
    plt.ylabel('Count')

    chart_path2 = 'static/genotype.png'
    plt.savefig(chart_path2)

    return render(request, 'statistics.html')

def user_records_view(request):
    
    if not request.user.userprofile.user_type == 'health_worker':
        return render(request, 'access_denied.html')

    users = CustomUser.objects.all()
    user_records = []

    form = MedicalRecordFilterForm(request.GET)
    condition = request.GET.get('condition')
    
    if condition:
        users = CustomUser.objects.filter(medicalrecord__disease=condition)
        

    for user in users:
        medical_records = MedicalRecord.objects.filter(user_id=user)
        user_records.append({'user': user, 'medical_records': medical_records})

    return render(request, 'user_records.html', {'user_records': user_records, 'form':form })

def search_health_workers(request):
    health_workers = CustomUser.objects.filter(userprofile__user_type='health_worker')
    return render(request, 'search_health_workers.html', {'health_workers': health_workers})

def book_appointment(request, health_worker_id):
    try:
        health_worker = get_object_or_404(CustomUser, id=health_worker_id)
    except Http404:
        return HttpResponse("Health Worker does not exist")

    if request.method == 'POST':
        form = AppointmentForm(request.user, request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.health_worker = health_worker
            appointment.save()

            subject = 'Appointment Request'
            message = render_to_string('appointment_notification.html', {'appointment': appointment})
            from_email = 'samuelomoyele777@gmail.com'
            to_email = health_worker.email

            email = EmailMessage(subject, strip_tags(message), from_email, [to_email])
            email.content_subtype = 'html'
            email.send()

            return redirect('appointment_success')
    else:
        form = AppointmentForm(request.user)

    context = {
        'health_worker': health_worker,
        'form': form,
    }

    return render(request, 'book_appointment.html', context)


def health_worker_dashboard(request):
    current_month = timezone.now().month
    appointments = Appointment.objects.filter(health_worker=request.user, status='pending')
    appointments_booked = appointments.filter(created_at__month=current_month, status='accepted').count()
    appointments_rejected = appointments.filter(created_at__month=current_month, status='rejected').count()

    if request.method == 'POST':
        form = AppointmentDecisionForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data['decision']
            
            if decision == 'accepted':
                appointment.status = 'accepted'
            else:
                appointment.status = 'rejected'
            appointment.save()
            return redirect('health_worker_dashboard')

    else:
        form = AppointmentDecisionForm()

    return render(request, 'health_worker_dashboard.html', {
        'appointments': appointments,
        'form': form,
        'appointments_booked': appointments_booked,
        'appointments_rejected': appointments_rejected,
    })