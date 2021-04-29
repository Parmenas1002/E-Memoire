from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name = "accounts_index"),
    path('register-student-2.0/',views.registerStudent,name = 'registerStudent'),
    path('register-teacher-2.0/',views.registerTeacher,name = 'registerTeacher'),
    path('login-partisans-2.0/',views.loginUser,name = 'loginUser'),
    path('dashboard-student-2.0/',views.dashboardStudent,name = 'dashboardStudent'),
    path('dashboard-teacher-2.0/',views.dashboardTeacher,name = 'dashboardTeacher'),
    path('profile-student-2.0/',views.profileStudent,name = 'profileStudent'),
    path('profile-teacher-2.0/',views.profileTeacher,name = 'profileTeacher'),
    path('logout/',views.logoutUser,name = 'logout'),
    path('ajax/load-faculty/', views.load_faculty, name='ajax_load_faculty'),
    path('ajax/load-entity/', views.load_entity, name='ajax_load_entity'),
    path('ajax/load-options/', views.load_options, name='ajax_load_options'),
    
]