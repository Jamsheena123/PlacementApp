from rest_framework import serializers
from Tpoapi.models import Student,Company,StudentProfile,Job,Application,Materials,InterviewSchedule

class StudentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Student
        fields=["id","First_name","Last_name","phone_no","email_address","username","password"]


    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)   
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentProfile    
        fields="__all__"


class  CompanySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Company
        fields=["id","name","description","industry","email_address","phone_no","Headquarters","founded","logo","website","username","password"]   
        
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields="__all__"  
        

class ApplicationSerializer(serializers.ModelSerializer):
    student=serializers.CharField(read_only=True)
    class Meta:
        model=Application
        fields="__all__"  
        
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Materials    
        fields="__all__"  
        
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=InterviewSchedule    
        fields="__all__"     