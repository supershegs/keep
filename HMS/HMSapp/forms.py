from django.contrib.auth.models import User
from HMSapp.models import *
#from . import models
#from models import Doctor, Patient, Appointment
from django import forms

#Admin signup
class admin_signup_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        Widgets = {
            'password': forms.PasswordInput()
        }

#Doctor signup form
class doctor_signup_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        Widgets = {
            'password': forms.PasswordInput()
        }
#Doctor profile/details form
class doctor_details_form(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'mobile', 'units', 'status', 'profile_pics']

#Patient signup form
class patient_signup_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        Widgets = {
            'password': forms.PasswordInput()
        }
#Patient profile/details form
class patient_details_form(forms.ModelForm):
    #To assigned a doctor
    DoctorAssignedID = forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Name and Unit", to_field_name="user_id")
    class Meta:
        model = Patient
        fields = ['address','mobile','status','symptoms','profile_pics']
#appointment form
class Appointment_form(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True), empty_label="Doctor Name and Unit", to_field_name="user_id")
    patient_id = forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True), empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields=['description', 'status']
#patient appointment form
class Patient_appointment_form(forms.ModelForm):
    doctor_id = forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True), empty_label="Doctor Name and Unit", to_field_name="user_id")
    class Meta:
        model= Appointment
        fields =['description', 'status']
        
#for contactUS
class Contactus_form(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows' : 3, 'cols' :30}))
    