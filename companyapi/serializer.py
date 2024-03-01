from rest_framework import serializers
from Tpoapi.models import Company,Job,Application,InterviewSchedule

class  CompanySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Company
        fields=["id","name","description","industry","email_address","phone_no","Headquarters","founded","logo","website","username","password"]    

    def create(self, validated_data):
        return Company.objects.create_user(**validated_data) 
    
    
class JobSerializer(serializers.ModelSerializer):
    posted_by=serializers.CharField(read_only=True)
    class Meta:
        model=Job
        fields="__all__"  
        

class ApplicationSerializer(serializers.ModelSerializer):
    student=serializers.CharField(read_only=True)
    class Meta:
        model=Application
        fields="__all__" 
        

class InterviewSheduleSerializer(serializers.ModelSerializer):
    company=serializers.CharField(read_only=True)
    application=serializers.CharField(read_only=True)
    class Meta:
        model=InterviewSchedule
        fields="__all__"     