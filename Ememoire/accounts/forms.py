from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator

from .models import Student, Option,Entity,Memoire,University,Faculty
CODE_ENSEIGNANT = "Enseignant2.0-2021"

class StudentCreationForm(forms.Form): #This form is used to create new Student as a user of our site
    lastName = forms.CharField(max_length=100,label="Nom")
    firstName = forms.CharField(max_length=100,label="Prénom")
    username = forms.CharField(max_length=100,label="Nom d'utilisateur"
    ,help_text="Ce nom vous servira pour la connexion.")
    email = forms.EmailField(label= "Adresse Mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    checkPassword = forms.CharField(widget=forms.PasswordInput, label='Confirmez votre mot de passe')
    
    def clean_checkPassword(self):
        password =self.cleaned_data['password']
        check_pass = self.cleaned_data ['checkPassword']

        if len(password)<8:
            raise forms.ValidationError('Votre mot de passe est trop court.')
        if password != check_pass:
            raise forms.ValidationError('Les mots de passe ne sont pas identiques')


class TeacherCreationForm(StudentCreationForm):
    teacherCode = forms.CharField(max_length=18,label="Code Enseignant")

    def clean_teacherCode(self):
        code =self.cleaned_data['teacherCode']    
        if code != CODE_ENSEIGNANT:
            raise forms.ValidationError("Le code Enseignant n'est pas correct. Veuillez respecter la casse !")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label= 'Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput,label ="Mot de passe")  
    
         

class EntityAddForm(forms.ModelForm): #This Form is used to add university,faculty and entity
    class Meta:
        model = Memoire
        fields = ['university','faculty','entity','option']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].required = False
        self.fields['university'].required = True
        self.fields['faculty'].required = True
        self.fields['entity'].required = True

        self.fields['faculty'].queryset = Option.objects.none()
        self.fields['entity'].queryset = Option.objects.none()
        self.fields['option'].queryset = Option.objects.none()

        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['faculty'].queryset = Faculty.objects.filter(university_id=university_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset"""
            
        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['entity'].queryset = Entity.objects.filter(faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset""

        if 'entity' in self.data:
            try:
                entity_id = int(self.data.get('entity'))
                self.fields['option'].queryset = Option.objects.filter(entity_id=entity_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset"""


class AddAvatarForm(forms.Form):
    avatar = forms.ImageField(required=False,label="Modifier")  

class ChangePasswordForm(forms.Form): 
    previous_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe actuel")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe")
    checkPassword = forms.CharField(widget=forms.PasswordInput, label='Confirmez le mot de passe')   

    def clean_checkPassword(self):
        password =self.cleaned_data['new_password']
        check_pass = self.cleaned_data ['checkPassword']

        if len(password)<8:
            raise forms.ValidationError('Votre mot de passe est trop court.')
        if password != check_pass:
            raise forms.ValidationError('Les mots de passe ne sont pas identiques')

    

    
        
