from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Hospital_units = [
    ('Family Depart', 'Family Physicians'),
    ('allergy Depart', 'Allergists/Immunologists'),
    ('Anesthesiology Depart', 'Anesthesiologists'),
    ('Heart Treatment Depart', 'Cardiologists'),
    ('Lower Abnonimal Depart', 'Colon and Rectal Surgeons'),
    ('Critical Care Depart', 'Critical Care Medicine Specialists'),
    ('Skincare Depart', 'Dermatologists'),
    ('Endocrinology Depart', 'Endocrinologists'),
    ('Gastroenterology Depart', 'Gastroenterologists'),
    ('geriatric Depart', 'Geriatric Medicine Specialists'),
    ('Emergency Medicine depart', 'Emergency Medicine Specialists'),
]

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pics = models.ImageField(upload_to='profilePics/Doctor_pics', null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    units = models.CharField(max_length=500, choices=Hospital_units, default='Family Depart')
    status = models.BooleanField(default=False)
    @property
    def getName(self):
        return self.user.first_name+ " "+ self.user.last_name
    @property
    def getID(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.units)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pics = models.ImageField(upload_to='profilePics/Patients_pics', null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    symptoms= models.CharField(max_length=100, null=False)
    Doctor_assigned_ID = models.PositiveIntegerField(null=True)
    Date_Admitted = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    @property
    def getName(self):
        return self.user.first_name+ " "+ self.user.last_name
    @property
    def getID(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
    
    
class Appointment(models.Model):
    patient_id=models.PositiveIntegerField(null=True)
    doctor_id=models.PositiveIntegerField(null=True)
    patient_name=models.CharField(max_length=40,null=True)
    doctor_name=models.CharField(max_length=40,null=True)
    appointment_date=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

class Patient_DischargeInformation(models.Model):
    patient_id=models.PositiveIntegerField(null=True)
    patient_name=models.CharField(max_length=40)
    assigned_doctor_name=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admit_date=models.DateField(null=False)
    release_date=models.DateField(null=False)
    day_spent=models.PositiveIntegerField(null=False)

    room_charge=models.PositiveIntegerField(null=False)
    medicine_cost=models.PositiveIntegerField(null=False)
    doctor_fees=models.PositiveIntegerField(null=False)
    Other_charges=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
