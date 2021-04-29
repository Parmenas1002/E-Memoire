from django.contrib import admin
from .models import Student,Entity,Option,Teacher,Memoire,University,Faculty
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name',"inscription_date")
    search_fields = ('last_name','first_name')
    ordering=('last_name',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name',"inscription_date")
    list_filter = ('inscription_date',)
    ordering=('last_name',)

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name','university')
    list_filter = ('university',)
    search_fields = ('university',)

class EntityAdmin(admin.ModelAdmin):
    list_display = ('name','faculty',)
    list_filter = ('faculty',)
    search_fields = ('faculty',)
    

class OptionAdmin(admin.ModelAdmin):
    list_display = ('name','entity',)
    list_filter = ('entity',)
    search_fields = ('entity',)

class MemoireAdmin(admin.ModelAdmin):
    list_display = ('topic','academicYear','supervisor','get_students','depositDay')
    list_filter = ('supervisor','academicYear','mention')
    

admin.site.register(Memoire,MemoireAdmin)   
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Entity,EntityAdmin)
admin.site.register(Option,OptionAdmin)
admin.site.register(University,UniversityAdmin)
admin.site.register(Faculty,FacultyAdmin)