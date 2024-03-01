from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.decorators import action

from Tpoapi.models import Student,Company,StudentProfile,Job,Application,Materials,InterviewSchedule
from studentapi.serializer import StudentSerializer,ProfileSerializer,CompanySerializer,JobSerializer,ApplicationSerializer,MaterialSerializer,InterviewSerializer



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
            return Response({"error": "student profile not found"}, status=404)
        
        qs = Student.objects.get(id=user_id)
        serializer = ProfileSerializer(qs)
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
        
    def list(self,request,*args,**kwargs):
        qs=Company.objects.all()
        serializer=CompanySerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        company_obj = Company.objects.get(id=id)
        company_serializer = CompanySerializer(company_obj)
        
        jobs_qs = Job.objects.filter(posted_by=company_obj)
        jobs_serializer = JobSerializer(jobs_qs, many=True)
        
        data = {
            'company': company_serializer.data,
            'jobs': jobs_serializer.data
        }
        return Response(data=data)


        
class jobView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=Job.objects.all()
        serializer=JobSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Job.objects.get(id=id)
        serializer=JobSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(methods=["post"],detail=True)
    def apply_job(self,request,*args,**kwargs):
        serializer=ApplicationSerializer(data=request.data)
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        job_id=kwargs.get("pk")
        job_obj=Job.objects.get(id=job_id)
        existing_applications = Application.objects.filter(job=job_obj, student=stud_obj)
        if existing_applications.exists():
            return Response(request,"you already applied for this post")
        else:
            if serializer.is_valid():
                serializer.save(job=job_obj,student=stud_obj)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
            

class ApplicationStatusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        qs=Application.objects.filter(student=stud_obj)
        serializer=ApplicationSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Application.objects.get(id=id)
        serializer=ApplicationSerializer(qs)
        return Response(data=serializer.data)
    

class InterviewView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]       
        
    def list(self,request,*args,**kwargs):
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        qs=InterviewSchedule.objects.filter(application__student=stud_obj)
        serializer=InterviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=InterviewSchedule.objects.get(id=id)
        serializer=InterviewSerializer(qs)
        return Response(data=serializer.data)
    
    
class MaterialView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]       
        
    def list(self,request,*args,**kwargs):
        qs=Materials.objects.all()
        serializer=MaterialSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Materials.objects.get(id=id)
        serializer=MaterialSerializer(qs)
        return Response(data=serializer.data)
    

