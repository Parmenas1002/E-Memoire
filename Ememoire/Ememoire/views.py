from django.shortcuts import render
from memoire.forms import EndDepositMemoryForOneStudentForm



def home(request):
    if request.method == 'POST':
        form =  EndDepositMemoryForOneStudentForm(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data['topic'])
    else :
        form =  EndDepositMemoryForOneStudentForm()
    return render(request,"pages/home.html",locals())