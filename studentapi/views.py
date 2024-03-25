from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.decorators import action
from rest_framework import status


from Tpoapi.models import Student,Company,StudentProfile,Job,Application,Materials,InterviewSchedule
from studentapi.serializer import StudentSerializer,ProfileSerializer,CompanySerializer,JobSerializer,ApplicationSerializer,MaterialSerializer,InterviewSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



class StudentCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Student")
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
        

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_type = user.user_type
        
        return Response(data={'status':1,'data':{'token': token.key,'user_type': user_type,}})
        

class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.student.id
        if user_id is None:
            return Response(request,data={'status':0,'msg':"student profile not found"}, status=status.HTTP_400_BAD_REQUEST)
        qs = Student.objects.get(id=user_id)
        serializer = ProfileSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})

    def put(self,request,*args,**kwargs): 
        id=request.user.student.id
        stud_obj=Student.objects.get(id=id)
        serializer=ProfileSerializer(data=request.data,instance=stud_obj)
        instance=Student.objects.get(id=id)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
        


class CompanyView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=Company.objects.all()
        serializer=CompanySerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
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
        return Response(data={'status':1,'data':data})



        
class jobView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=Job.objects.all()
        serializer=JobSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Job.objects.get(id=id)
        serializer=JobSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    
    @action(methods=["post"],detail=True)
    def apply_job(self,request,*args,**kwargs):
        serializer=ApplicationSerializer(data=request.data)
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        job_id=kwargs.get("pk")
        job_obj=Job.objects.get(id=job_id)
        existing_applications = Application.objects.filter(job=job_obj, student=stud_obj)
        if existing_applications.exists():
            return Response(request,data={'status':0,'msg':"you already applied for this post"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save(job=job_obj,student=stud_obj)
                return Response(data={'status':1,'data':serializer.data})
            else:
                error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
                return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
            

class ApplicationStatusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        qs=Application.objects.filter(student=stud_obj)
        serializer=ApplicationSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Application.objects.get(id=id)
        serializer=ApplicationSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    

class InterviewView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]       
        
    def list(self,request,*args,**kwargs):
        stud_id=request.user.id
        stud_obj=Student.objects.get(id=stud_id)
        qs=InterviewSchedule.objects.filter(application__student=stud_obj)
        serializer=InterviewSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=InterviewSchedule.objects.get(id=id)
        serializer=InterviewSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    
class MaterialView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]       
        
    def list(self,request,*args,**kwargs):
        qs=Materials.objects.all()
        serializer=MaterialSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Materials.objects.get(id=id)
        serializer=MaterialSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    

