from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from .forms import StudentCreationForm,TeacherCreationForm,LoginForm,EntityAddForm,AddAvatarForm
from .models import Student, Option, Teacher,Memoire,Faculty,Entity


# Create your views here.

def index(request):
    return render(request,"accounts/index.html")

def registerStudent(request):
    errorMessage = ""
    new_memoire = Memoire()
    envoi= False
    form = StudentCreationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        lastName = form.cleaned_data['lastName']
        firstName = form.cleaned_data['firstName']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User()
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except user.DoesNotExist:
                user = User.objects.create_user(username,email, password)
                newStudent = Student.objects.create(user = user)
                newStudent.last_name = lastName
                newStudent.first_name = firstName
                new_memoire.save()
                newStudent.memoire.add(new_memoire)
                newStudent.save() 
                envoi=True
            else :
                errorMessage  = "Un utilisateur possède déjà cette addresse mail."
        else :
            errorMessage  = "Un utilisateur possède déjà ce nom d'utilisateur."
                
           
    if envoi ==True :
        login(request,user)
        return redirect('dashboardStudent') 
    return render(request,'accounts/register_student.html',locals())

def registerTeacher(request):
    errorMessage = ""
    envoi= False
    form = TeacherCreationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        lastName = form.cleaned_data['lastName']
        firstName = form.cleaned_data['firstName']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User()
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except user.DoesNotExist:
                user = User.objects.create_user(username,email, password)
                newTeacher = Teacher.objects.create(user = user)
                newTeacher.last_name = lastName
                newTeacher.first_name = firstName
                newTeacher.save() 
                envoi=True
            else :
                errorMessage  = "Un utilisateur possède déjà cette addresse mail."
        else :
            errorMessage  = "Un utilisateur possède déjà ce nom d'utilisateur."
                
           
    if envoi ==True :
        login(request,user)
        return redirect('dashboardTeacher')  
    return render(request,'accounts/register_teacher.html',locals())

def loginUser(request):
    errorMessage = ""
    envoi = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User()
            
            try:
                user = User.objects.get(username=username)
            except user.DoesNotExist:
                errorMessage = "Aucun utilisateur n'a été enregistré avec le nom " +username + "."
            else :
                user = authenticate(username = username, password = password)
                if user == None :
                    errorMessage = "Votre mot de passe est incorrect."
                else :
                    login(request,user)
                    currentStudent=Student()
                    currentStudent=Teacher()
                    try:
                        currentStudent = Student.objects.get(user = user)                        
                    except  Exception as e:                                     
                        return redirect('dashboardTeacher')
                         
                    else:                                          
                        return redirect('dashboardStudent')
                          
    else: 
        form = LoginForm()
    return render(request,'accounts/login_user.html',locals())


@login_required
def dashboardStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentStudent = Student.objects.get(user = user)
    studentmemoires = currentStudent.memoire.all()
    first_deposit= False
    if len(studentmemoires) ==1:
        first_deposit = True
        unique_memoire = studentmemoires[0]
        form = EntityAddForm()
        if request.method == 'POST':
            form = EntityAddForm(request.POST)
            if form.is_valid():
                unique_memoire.university = form.cleaned_data['university']
                unique_memoire.faculty = form.cleaned_data['faculty']
                unique_memoire.entity  = form.cleaned_data['entity']
                unique_memoire.option = form.cleaned_data['option']
                unique_memoire.save()
        
    return render(request, 'accounts/dashboard_student.html',locals())
@login_required
def dashboardTeacher(request):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentTeacher = Teacher.objects.get(user = user)    
    exist_memoire = False
    if len(currentTeacher.get_list_memoires()) >=1:
        memoires = currentTeacher.get_list_memoires()
        exist_memoire = True

    return render(request, 'accounts/dashboard_teacher.html',locals())

@login_required
def profileStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentStudent = Student.objects.get(user = user)
    total = len(currentStudent.memoire.all()) 
    valid = len(currentStudent.memoire.filter(stateAfter=True))
    no_valid = total-valid
    avartarForm = AddAvatarForm()
    changePassForm = PasswordChangeForm(user= request.user)
    if request.method == 'POST':    
        if "change_avatar" in request.POST :
            avartarForm = AddAvatarForm(request.POST,request.FILES)
            if avartarForm.is_valid():
                avatar = avartarForm.cleaned_data['avatar']
                if avatar != None :
                    currentStudent.avatar = avatar
                    currentStudent.save()
                
        if "change_password" in request.POST :
            changePassForm = PasswordChangeForm(user=request.user, data=request.POST)
            print(changePassForm)
            if changePassForm.is_valid():
                user = changePassForm.save()
                update_session_auth_hash(request, user)  # Important!    
            else:
                print("Change No")
        
    return render(request, 'accounts/profile_student.html',locals())
    

@login_required
def profileTeacher(request):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentTeacher = Teacher.objects.get(user = user) 
    total = len(currentTeacher.get_list_memoires()) 
    valid = len(currentTeacher.get_list_memoires().filter(stateAfter=True))
    no_valid = total-valid

    avartarForm = AddAvatarForm()
    changePassForm = PasswordChangeForm(user= request.user)
    if request.method == 'POST':    
        if "change_avatar" in request.POST :
            avartarForm = AddAvatarForm(request.POST,request.FILES)
            if avartarForm.is_valid():
                avatar = avartarForm.cleaned_data['avatar']
                if avatar != None :
                    currentTeacher.avatar = avatar
                    currentTeacher.save()
                
        if "change_password" in request.POST :
            changePassForm = PasswordChangeForm(user=request.user, data=request.POST)
            print(changePassForm)
            if changePassForm.is_valid():
                user = changePassForm.save()
                update_session_auth_hash(request, user)  # Important!    
            else:
                print("Change No")
        
    return render(request, 'accounts/profile_teacher.html',locals())

def logoutUser(request):
    logout(request)
    return redirect('loginUser')


# AJAX
def load_faculty(request):
    university_id = request.GET.get('university_id')
    faculties = Faculty.objects.filter(university_id=university_id)
    return JsonResponse(list(faculties.values('id', 'name')), safe=False)

def load_entity(request):
    faculty_id = request.GET.get('faculty_id')
    entities = Entity.objects.filter(faculty_id=faculty_id)
    return JsonResponse(list(entities.values('id', 'name')), safe=False)

def load_options(request):
    entity_id = request.GET.get('entity_id')
    options = Option.objects.filter(entity_id=entity_id)
    return JsonResponse(list(options.values('id', 'name')), safe=False)

