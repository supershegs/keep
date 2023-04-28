from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.Home, name='home'),
    path('admin_main.html', views.admin_view, name='admin_main'),
    path('doctor_main.html',views.doctor_view, name='doctor_main'),
    path('patient_main.html', views.patient_view, name='patient_main'),
    
    path('admin_signup.html',views.admin_signup_view, name='admin_signup'),
    path('doctor_signup.html', views.doctor_signup_view, name='doctor_signup'),
    path('patient_signup.html', views.patient_signup_view, name='patient_signup'),
    
    #another  way of calling ur routes/views using the inbuit class LoginView & LogoutView
    path('admin_login', LoginView.as_view(template_name='admin_login.html')),
    path('doctor_login', LoginView.as_view(template_name='doctor_login.html')),
    path('patient_login', LoginView.as_view(template_name='patient_login.html')),


    path('after_login', views.after_login_view,name='after_login'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),
    path('admin_dashboard', views.admin_dashboard_view, name='admin_dashboard'),

    path('admin_dashboard', views.admin_dashboard_view,name='admin_dashboard'),
]