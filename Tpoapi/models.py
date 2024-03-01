from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    user_type_choices=[ 
        ('Tpo', 'Tpo'),
        ('Company' ,'Company'),
        ('Student' ,'Student'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='Tpo')

class TPO(CustomUser):
    name = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class Student(CustomUser):
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)

    
    def __str__(self):
        return self.First_name
    
class Company(CustomUser):
    name = models.CharField(max_length=100)
    description = models.TextField()    
    industry = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    Headquarters = models.TextField()
    founded=models.PositiveIntegerField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    profile=models.ImageField(blank=True,null=True)    


    def __str__(self):
        return self.name   


class Job(models.Model):
    posted_by = models.ForeignKey(Company,on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()       

    
class Materials(models.Model):
    topic= models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    video=models.FileField(upload_to="videos")
    posted_date=models.DateTimeField(auto_now_add=True)


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name="profile",null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100,null=True)
    batch_year = models.PositiveIntegerField(null=True)
    skills = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    address = models.TextField(null=True)
    resume=models.FileField(upload_to="images",null=True)



def create_profile(sender,created,instance,**kwargs):
    if created:
        StudentProfile.objects.create(student=instance)

post_save.connect(create_profile,sender=Student)





class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

class InterviewSchedule(models.Model):
    tpo = models.ForeignKey('TPO', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)




