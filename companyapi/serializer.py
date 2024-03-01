from rest_framework import serializers
from Tpoapi.models import Company

class  CompanySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Company
        fields=["id","name","description","industry","email_address","phone_no","Headquarters","founded","logo","website","username","password"]    

    def create(self, validated_data):
        return Company.objects.create_user(**validated_data)      