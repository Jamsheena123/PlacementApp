from django.shortcuts import render
from studentapi.serializer import StudentSerializer,ProfileSerializer,CompanySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import permissions
from rest_framework import authentication
from Tpoapi.models import Student,Company



class StudentCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Student")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        

class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.student.id
        if user_id is None:
            return Response({"error": "Customer profile not found"}, status=404)
        
        qs = Student.objects.get(id=user_id)
        serializer = StudentSerializer(qs)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs): 
        id=request.user.student.id
        stud_obj=Student.objects.get(id=id)
        serializer=ProfileSerializer(data=request.data,instance=stud_obj)
        instance=Student.objects.get(id=id)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

        
class CompanyView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CompanySerializer
        
    def list(self,request,*args,**kwargs):
        qs=Company.objects.all()
        serializer=CompanySerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Company.objects.get(id=id)
        serializer=CompanySerializer(qs)
        return Response(data=serializer.data)
    

    

