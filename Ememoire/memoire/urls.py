from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = "memoire_index"),
    path('end-deposit-partisans-2.0-1',views.endDepositForOneStudent, name = "endDepositForOneStudent"),
    path('end-deposit-partisans-2.0-2',views.endDepositForTwoStudent, name = "endDepositForTwoStudent"),
    path('deposit-partisans-2.0-1',views.depositForOneStudent, name = "depositForOneStudent"),
    path('deposit-partisans-2.0-2',views.depositForTwoStudent, name = "depositForTwoStudent"),
    path('teacher-view-memory-2.0/<int:id>',views.viewTeacher, name = "viewTeacher"),
    path('student-view-memory-2.0/<int:id>',views.viewStudent, name = "viewStudent"),
]