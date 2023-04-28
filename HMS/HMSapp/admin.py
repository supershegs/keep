from django.contrib import admin

# Register your models here.

from . import models

#class Doctor_Admin(admin.ModelAdmin):
#    pass

#admin.site.register(models.Doctor, Doctor_Admin)
admin.site.register(models.Doctor)
admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.Patient_DischargeInformation)
