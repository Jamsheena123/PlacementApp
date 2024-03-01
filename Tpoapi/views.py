from django.shortcuts import render
from rest_framework.views import APIView
from Tpoapi.serializer import TpoSerializer,StudentSerializer,CompanySerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from Tpoapi.models import Student,Company
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action



class TpoCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=TpoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Tpo")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class StudentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = StudentSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Student.objects.all()
        serializer=StudentSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Student.objects.get(id=id)
        serializer=StudentSerializer(qs)
        return Response(data=serializer.data)
    
    def update(self,request,*args,**kwargs):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
@action(methods=['post'], detail=True)
def add_materials(self, request, *args, **kwargs):
        student_id = kwargs.get("pk") 
        material = request.data.get("material")  
        if not material:
            return Response({"error": "Material data is missing."}, status=400)
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=404)
        
        student.study_materials.append(material)
        student.save()
        return Response({"message": f"Material '{material}' added to student ID {student_id}."}, status=200)

    
class CompanycreateView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CompanySerializer
        
    def list(self,request,*args,**kwargs):
        qs=Company.objects.all()
        serializer=CompanySerializer(qs,many=True)
        return Response(data=serializer.data)

