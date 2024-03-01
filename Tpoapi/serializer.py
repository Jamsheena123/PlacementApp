from rest_framework import serializers
from Tpoapi.models import TPO,Student,Company

class TpoSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=TPO
        fields=["id","name","phone_no","email_address","username","password"]


    def create(self,validated_data):
        return TPO.objects.create_user(**validated_data)

class StudentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Student
        fields=["id","First_name","Last_name","phone_no","email_address","username","password"]


    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)     



class  CompanySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Company
        fields=["id","name","description","industry","email_address","phone_no","Headquarters","founded","logo","website","username","password"]        

 
    


