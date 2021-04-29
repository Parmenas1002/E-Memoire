from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import EndDepositMemoryForOneStudentForm,EndDepositMemoryForTwoStudentForm,OneStudentDepositForm,TwoStudentDepositForm,TeacherModifForm,StudentModifForm
from accounts.models import Student,Memoire,Teacher

#==============================================================Controller Tools============================================
def verification(user):
    currentStudent= Student()
    try:
        currentStudent = Student.objects.get(user = user)                        
    except  Exception:    
        return False
    else: 
        return True  

def getStudent(username,password):
    user = authenticate(username = username, password = password)
    currentStudent = Student.objects.get(user = user)
    return currentStudent

def patnerVerification(username,password,currentStudent):
    user = User()
    user = authenticate(username = username, password = password)
    if user == None :
        return False, "Les identifiants de votre partenaire sont incorrects."
    else :
        student_verify = verification(user)
        if student_verify == True:
            if currentStudent == user:
                return False, "Vous essayer de vous rajouter comme binome."
            else :
                return True, "Un autre étudiant a été bien ajouté"
        else:
            return False, "Vous ne pouvez pas ajouté un enseignant à votre projet."


#==================================================================================

def index(request):
    memoires = Memoire.objects.filter(stateAfter=True)
    
    return render (request, "memoire/index.html",locals())

#========================= Finalisation du dépot pour un seul étudiant
@login_required
def endDepositForOneStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password) 
    currentStudent = Student.objects.get(user = user)
    studentmemoires = currentStudent.memoire.all()
    errorMessage = ""
    envoi =False 
    unique_memoire = studentmemoires[0]
    if request.method == 'POST':
        form =  EndDepositMemoryForOneStudentForm(request.POST,request.FILES)
        if form.is_valid():
            unique_memoire.topic = form.cleaned_data['topic']
            unique_memoire.document = form.cleaned_data['document']                
            unique_memoire.supervisor = form.cleaned_data['supervisor']
            unique_memoire.save()
            envoi = True
    else :
        form =  EndDepositMemoryForOneStudentForm()
    if envoi ==True:
        return redirect('dashboardStudent')
        
    return render(request, "memoire/end_one.html",locals())

#=========================Dépot complet de mémoire pour un seul étudiant
@login_required
def depositForOneStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password) 
    currentStudent = Student.objects.get(user = user)
    errorMessage = ""
    envoi =False 
    new_memoire = Memoire()
    if request.method == 'POST':
        form =  OneStudentDepositForm(request.POST,request.FILES)
        if form.is_valid():
            new_memoire.university =form.cleaned_data['university']
            new_memoire.faculty = form.cleaned_data['faculty']
            new_memoire.entity = form.cleaned_data['entity']
            new_memoire.option = form.cleaned_data['option']
            new_memoire.topic = form.cleaned_data['topic']
            new_memoire.supervisor = form.cleaned_data['supervisor']
            new_memoire.document = form.cleaned_data['document']                            
            new_memoire.save()
            currentStudent.memoire.add(new_memoire)
            currentStudent.save() 
            envoi = True
    else :
        form =  OneStudentDepositForm()
    if envoi ==True:
        return redirect('dashboardStudent')
        
    return render(request, "memoire/deposit_one.html",locals())
    
#================================= Finalisation de dépot pour deux étudiants
@login_required
def endDepositForTwoStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password) 
    currentStudent = Student.objects.get(user = user)
    studentmemoires = currentStudent.memoire.all()
    errorMessage = ""
    envoi =False 
    unique_memoire = studentmemoires[0]
    if request.method == 'POST':
        form =  EndDepositMemoryForTwoStudentForm(request.POST,request.FILES)               
        if form.is_valid():
            indicator, message = patnerVerification(form.cleaned_data['patnerUsername'],form.cleaned_data['patnerPassword'],user)
            if indicator == False:
                errorMessage = message
            else :
                patner = getStudent(form.cleaned_data['patnerUsername'],form.cleaned_data['patnerPassword'])                
                unique_memoire.topic = form.cleaned_data['topic']
                unique_memoire.document = form.cleaned_data['document']                
                unique_memoire.supervisor = form.cleaned_data['supervisor']
                unique_memoire.save()      
                patner.memoire.add(unique_memoire)
                patner.save()  
                envoi = True               
    else :
        form =  EndDepositMemoryForTwoStudentForm()
    if envoi ==True:
        return redirect('dashboardStudent')
    return render(request, "memoire/end_two.html",locals())

#===================================Dépot de mémoire pour deux persones
@login_required
def depositForTwoStudent(request):
    user = User.objects.get(username = request.user.username, password=request.user.password) 
    currentStudent = Student.objects.get(user = user)
    errorMessage = ""
    envoi =False 
    new_memoire = Memoire()
    if request.method == 'POST':
        form =  TwoStudentDepositForm(request.POST,request.FILES)
        if form.is_valid():
            indicator, message = patnerVerification(form.cleaned_data['patnerUsername'],form.cleaned_data['patnerPassword'],user)
            print(indicator,message)
            if indicator == False:
                errorMessage = message
            else :
                patner = getStudent(form.cleaned_data['patnerUsername'],form.cleaned_data['patnerPassword'])
                new_memoire.university =form.cleaned_data['university']
                new_memoire.faculty = form.cleaned_data['faculty']
                new_memoire.entity = form.cleaned_data['entity']
                new_memoire.option = form.cleaned_data['option']
                new_memoire.topic = form.cleaned_data['topic']
                new_memoire.supervisor = form.cleaned_data['supervisor']
                new_memoire.document = form.cleaned_data['document']                            
                new_memoire.save()
                currentStudent.memoire.add(new_memoire)
                patner.memoire.add(new_memoire)
                patner.save() 
                currentStudent.save() 
                envoi = True
                
    else :
        form =  TwoStudentDepositForm()
    
    if envoi ==True:
        return redirect('dashboardStudent') 
    return render(request, "memoire/deposit_two.html",locals())

@login_required
def viewTeacher(request,id):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentTeacher = Teacher.objects.get(user = user)
    memoire = get_object_or_404(Memoire, id=id)
    if request.method == 'POST':
        form = TeacherModifForm(request.POST)
        if form.is_valid():
            memoire.middleClass =form.cleaned_data['middleClass']
            memoire.mention = form.cleaned_data['mention']
            memoire.stateAfter = form.cleaned_data['stateAfter']
            memoire.save()

    else:
        form = TeacherModifForm()
    return render(request,"memoire/view_teacher.html",locals())
@login_required
def viewStudent(request,id):
    user = User.objects.get(username = request.user.username, password=request.user.password)      
    currentStudent = Student.objects.get(user = user)
    memoire = get_object_or_404(Memoire, id=id)
    if request.method == 'POST':    
        form = StudentModifForm(request.POST)
        if form.is_valid():
            print("Yes")
        else:
            print("No")

    else:
        form = StudentModifForm()
    
    return render(request,"memoire/view_student.html",locals())