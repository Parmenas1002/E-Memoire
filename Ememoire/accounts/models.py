from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import datetime

#====================== Variables
current_year = datetime.datetime.now().date().year
previous = "{}-{}".format((current_year-1),current_year)

ACADEMIC_YEAR = (
    (previous,previous),
)

MENTION_OPTIONS = (
    ('Passable','Passable'),
    ('Assez-bien','Assez-bien'),
    ('Bien','Bien'),
    ('Très-bien','Très-bien'),
    ('Excellente','Excellente')
)

#=================================

#================================ Models

# Modèle des universités
class University(models.Model):
    name = models.CharField(max_length=110, verbose_name= "Intitulé de l'Université")

    class Meta():
        verbose_name = "Université"
        ordering = ['name']    
    def __str__(self):
        return self.name

# (Ce modèle réprésente les différentes écoles, facultés et instituts au sein d'une université)
class Faculty(models.Model):
    name = models.CharField(max_length=110, verbose_name= "Intitulé de le l'école/Institut/Faculté")
    university = models.ForeignKey(University, on_delete= models.CASCADE,verbose_name= "Université")

    class Meta():
        verbose_name="Ecole/Institut/Faculté"
        ordering = ['name']

    def __str__(self):
        return str(self.university) + "/" + self.name  


# Ce modèle est celui des différentes filières au sein d'une école, faculté ou un institut
class Entity(models.Model):
    name = models.CharField(max_length=40, verbose_name="Intitulé de la Filière")
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE, verbose_name ="Ecole/Institut/Faculté")

    class Meta():
        verbose_name = "Filière"
        ordering = ['name']

    def __str__(self):
        return str(self.faculty)+ '/' + self.name

# Ce modèle représente le modèle des options des différentes filières   
class Option(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE,verbose_name="Filière")
    name = models.CharField(max_length=40,verbose_name="Option")

    class Meta():
        ordering = ['entity__name']

    def __str__(self):
        return  self.name


# Modèle Enseignants
class Teacher(models.Model):
    user = models.OneToOneField(User, default= 0, on_delete = models.CASCADE)
    last_name= models.CharField(default="", max_length=100,verbose_name="Nom")
    first_name = models.CharField(default="", max_length=100,verbose_name="Prénom")
    avatar = models.ImageField(default = 'default.png',upload_to = 'avatar/',null=True, blank=True)
    inscription_date = models.DateTimeField(auto_now_add=True,verbose_name="Date d'Inscription")

    
    class Meta():
        verbose_name = "Enseignant"

    def get_list_memoires(self):
        return self.memoire_set.all()

    def __str__(self):
        return self.last_name + " " + self.first_name
    


# Modèle  mémoires
class Memoire(models.Model):
    topic = models.CharField(max_length=220,verbose_name="Thème du mémoire",blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Université")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Ecole/Faculté/Institut")
    entity = models.ForeignKey(Entity,default="", on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Filière")
    option = models.ForeignKey(Option,default="", on_delete=models.SET_NULL, blank=True, null=True)
    academicYear = models.CharField(max_length=20,default=previous, verbose_name="Année Académique",choices=ACADEMIC_YEAR)
    supervisor = models.CharField(max_length=120,verbose_name="Superviseur",blank=True, null=True)
    middleClass = models.FloatField(default=0, verbose_name="Note obtenue",null=True, blank=True)
    mention = models.CharField(max_length=20, verbose_name="Mention",choices=MENTION_OPTIONS,null=True, blank=True)
    stateBefore = models.BooleanField(default=False,verbose_name="Statut avant la Soutenance")
    stateAfter = models.BooleanField(default=False, verbose_name="Statut après la soutenance")
    depositDay = models.DateTimeField(auto_now_add=True,verbose_name="Date de dépôt")
    abstract = models.TextField(null=True,blank=True,verbose_name="Résumé du Mémoire")
    teachers = models.ManyToManyField(Teacher,blank=True,verbose_name="Enseignants assignés")
    presentationImage = models.ImageField(upload_to = 'image_memoire/',verbose_name= "Image de présentation",null=True,blank=True)
    document = models.FileField(upload_to = "document_memoire/",verbose_name = "Document du Mémoire",validators = [FileExtensionValidator(allowed_extensions=['pdf'],message="Veuillez charger uniquement des documents de type pdf.")])
    video = models.FileField(upload_to = "video_memoire/",verbose_name = "Vidéo du Mémoire",validators = [FileExtensionValidator(allowed_extensions=['mp4'],message="Veuillez charger uniquement des documents de type mp4.")],null=True,blank=True )
    
    class Meta():
        verbose_name = "Mémoire"
        ordering=['-depositDay']
    
    def get_students(self):
        students = self.student_set.all()
        student_char_list = ""
        i=0
        for student in students:
            if i==0 :            
                student_char_list += str(student)
            else :
                student_char_list += " & " + str(student)
            i=i+1
        return student_char_list
        
    def __str__(self):
        if self.topic ==None :
            return "Mémoire non rempli"
        else:
            return self.topic
    
    
# Modèle Etudiant
class Student(models.Model):
    user = models.OneToOneField(User, default= 0, on_delete = models.CASCADE)
    last_name= models.CharField(default="", max_length=100,verbose_name="Nom")
    first_name = models.CharField(default="", max_length=100,verbose_name="Prénom") 
    avatar = models.ImageField(default = 'default.png',upload_to = 'avatar/',null=True, blank=True)   
    inscription_date = models.DateTimeField(auto_now_add=True,verbose_name="Date d'Inscription")
    memoire = models.ManyToManyField(Memoire,blank=True,verbose_name="Mémoires")    

    class Meta():
        verbose_name = "Etudiant"
    def __str__(self):
        return self.last_name + " " + self.first_name


    






    












    