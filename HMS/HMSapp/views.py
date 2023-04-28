from django.shortcuts import render,redirect, reverse
from . import forms, models
from django.contrib import messages
#from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.mail import send_mail
from django.contrib.auth.decorators import  login_required, user_passes_test
from datetime import date
#from django.conf import settings
from django.db.models import Q

# Create your views here.
def Home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')
    return render(request, 'index.html')

def admin_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')
    return render(request, 'admin_main.html')


def doctor_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')
    return render(request, 'doctor_main.html')

def patient_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')
    return render(request, 'patient_main.html')

#register admin
def admin_signup_view(request):
    form = forms.admin_signup_form()
    if request.method=='POST':
        form = forms.admin_signup_form(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            messages.info(request, 'Registration successful. Please login below!')
            return HttpResponseRedirect('admin_login', {'messages': messages})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field.title()}: {error}")
    return render(request,  'admin_signup.html', {'form': form})

#register doctor
def doctor_signup_view(request):
    user_form =  forms.doctor_signup_form()
    doctor_form = forms.doctor_details_form()
    Doctor_dict= {'user_form': user_form, 'doctor_form': doctor_form }
    if  request.method  =='POST':
        # import pdb
        # pdb.set_trace()
        
        user_form = forms.doctor_signup_form(request.POST)
        doctor_form = forms.doctor_details_form(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group =Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.info(request, 'Registration successful. Please login below!')
            return HttpResponseRedirect('doctor_login',{'messages': messages})
        else:
            print('error for doctor user form =', user_form.errors, '-------')
            print('error from doctor details form =',doctor_form.errors, '------') 
            print('error', doctor_form.fields['units'])
            
            for field, errors in doctor_form.errors.items():
                for error in errors:
                    messages.error(request,f"{field.title()}: {error}")
                return render(request, 'doctor_signup.html')
    return render(request, 'doctor_signup.html', context=Doctor_dict)

#register patient
def patient_signup_view(request):
    user_form = forms.patient_signup_form()
    patient_form = forms.patient_details_form()
    Patient_dict = {'user_form': user_form, 'patient_form': patient_form}
    if request.method=='POST':
        user_form= forms.patient_signup_form(request.POST)
        patient_form = forms.patient_details_form(request.POST, request.FILES)
        if user_form.is_valid and patient_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient=patient_form.save(commit=False)
            patient.user = user
            patient.DoctorAssignedID= request.POST.get('DoctorAssignedID')
            patient = patient.save()
            my_patient_group=Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
            messages.info(request, 'Registration successful. Please login below!')
            return HttpResponseRedirect('patient_login', {'messages': messages})
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request,f"{field.title()}: {error}")
        
    return render(request, 'patient_signup.html', context=Patient_dict)

#checking if user is a doctor/patient/admit
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#after Entering credential(username and password) to check for  either admin or doctor or patient 
#along with  the appoval stated with ADMIN
def after_login_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_dashboard')
        elif is_doctor(request.user):
            account_approval = models.Doctor.objects.all().filter(user_id = request.user.id, status=True)
            if account_approval:
                return redirect('doctor_dashboard')
            else:
                return render(request, 'doctor_profile_approval_pending.html')
            
        elif is_patient(request.user):
            account_approval = models.Patient.objects.all().filter(user_id = request.user.id, status=True)
            if account_approval:
                return redirect('patient_dashboard')
            else:
                return render(request,'patient_profile_approval_pending.html')
        else:
            return HttpResponse('Unknown User Type, Login via app')
    else:
        if request.user.is_authenticated:
            groups = request.user.groups.all()
            return  HttpResponse('E choke, login properly, {groups}', {'groups': groups})
            
    #Admin dashboard page
        
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
        
def admin_dashboard_view(request):
    #for both doctors and patients in admin dashboard.
    doctors= models.Doctor.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')
    
    #for the doctors, patient, appointment: checking counts and pending approval
    doctor_count= models.Doctor.objects.all().filter(status=True).count()
    pending_doctor_count = models.Doctor.objects.all().filter(status=False).count()
    
    patient_count= models.Patient.objects.all().filter(status=True).count()
    pending_patient_count= models.Patient.objects.all().filter(status=True).count()
    
    appointment_count = models.Appointment.objects.all().filter(status=True).count()
    pending_appointment_count= models.Appointment.objects.all().filter(status=False).count()
    
    Admin_dict = {
        'doctors': doctors,
        'patients': patients,
        'doctor_count': doctor_count,
        'pending_doctor_count': pending_doctor_count,
        'patient_count': patient_count,
        'pending_patient_count': pending_patient_count,
        'appointment_count': appointment_count,
        'pending_appointment_count': pending_appointment_count
    }
    
    return render(request, 'admin_dashboard.html', context=Admin_dict)

# this view for sidebar click on admin page
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'admin_doctor.html')



@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin_view_doctor')

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    
    user_form =forms.doctor_signup_form(instance=user)
    doctor_form =forms.doctor_details_form(request.FILES, instance=doctor)
    update_doctor_dict ={'user_form': user_form, 'doctor_form': doctor_form}
    if request.method=='POST':
        user_form = forms.doctor_signup_form(request.POST, instance=user)
        doctor_form =forms.doctor_details_form(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin_view_doctor')
    return render(request, 'admin_update_doctor.html', context=update_doctor_dict)
  
    
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    user_form = forms.doctor_signup_form()
    doctor_form = forms.doctor_details_form()
    admin_add_doctor_dict = {'user_form':user_form,'doctor_form':doctor_form}

    if request.method=='POST':
        user_form=forms.doctor_signup_form(request.POST)
        doctor_form=forms.doctor_details_form(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            doctor=doctor_form.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin_view_ doctor')
    return render(request,'hospital/admin_add_doctor.html',context = admin_add_doctor_dict)

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #show the doctor that needs approval under admin
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'admin_approve_doctor.html', {'doctors':doctors}) 

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin_approve_doctor'))


@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin_approve_doctor')

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'admin_view_doctor_specialisation.html', {'doctors': doctors})
            
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients= models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_view_patient.html', {'patients': patients})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_view_patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    user_form=forms.patient_signup_form(instance=user)
    patient_form=forms.patient_details_form(request.FILES,instance=patient)
    update_patient_view_dict={'user_form':user_form,'patient_form':patient_form}
    if request.method=='POST':
        user_form=forms.patient_signup_form(request.POST,instance=user)
        patient_form=forms.patient_details_form(request.POST,request.FILES,instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            patient=patient_form.save(commit=False)
            patient.status=True
            patient.DoctorAssignedID=request.POST.get('DoctorAssignedID')
            patient.save()
            return redirect('admin_view_patient')
    return render(request,'admin_update_patient.html',context=update_patient_view_dict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    user_form=forms.patient_signup_form()
    patient_form=forms.patient_details_form()
    admin_add_patient_dict={'userForm':user_form,'patient_form':patient_form}
    if request.method=='POST':
        user_form=forms.patient_signup_form(request.POST)
        patient_form=forms.patient_details_form(request.POST,request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            patient=patient_form.save(commit=False)
            patient.user=user
            patient.status=True
            patient.DoctorAssignedID=request.POST.get('DoctorAssignedID')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin_view_patient')
    return render(request,'admin_add_patient.html',context=admin_add_patient_dict)
