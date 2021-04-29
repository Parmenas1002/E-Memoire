from django import forms
from django.core.validators import FileExtensionValidator
from accounts.models import Option,Entity,Memoire,University,Faculty

class EndDepositMemoryForOneStudentForm(forms.Form):
    topic =forms.CharField(max_length=220,label="Thème du mémoire") 
    supervisor = forms.CharField(max_length=120,label="Superviseur du Mémoire")
    document = forms.FileField(label="Document du Mémoire", validators=[FileExtensionValidator(allowed_extensions=['pdf'],message="Les documents de mémoires doivent être des fichiers pdf")])


class EndDepositMemoryForTwoStudentForm(EndDepositMemoryForOneStudentForm):
    patnerUsername = forms.CharField(max_length=100,label="Nom d'utilisateur de votre binôme" )
    patnerPassword = forms.CharField(widget=forms.PasswordInput,label="Mot de passe de votre binôme")
    

class OneStudentDepositForm(forms.ModelForm): #This Form is used to add university,faculty and entity
    class Meta:
        model = Memoire
        fields = ['university','faculty','entity','option','topic','supervisor','document']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].required = False
        self.fields['university'].required = True
        self.fields['faculty'].required = True
        self.fields['entity'].required = True
        self.fields['topic'].required = True
        self.fields['supervisor'].required = True
        self.fields['document'].required = True

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

class TwoStudentDepositForm(OneStudentDepositForm):
    patnerUsername = forms.CharField(max_length=100,label="Nom d'utilisateur de votre binôme" )
    patnerPassword = forms.CharField(widget=forms.PasswordInput,label="Mot de passe de votre binôme")


class TeacherModifForm(forms.ModelForm):
    class Meta:
        model = Memoire
        fields = ['middleClass','mention','stateAfter']

class StudentModifForm(forms.ModelForm):
    class Meta:
        model = Memoire
        fields = ['presentationImage','abstract','video','document']