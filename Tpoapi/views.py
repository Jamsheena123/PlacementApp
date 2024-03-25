from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status


from Tpoapi.serializer import TpoSerializer,StudentSerializer,CompanySerializer,MaterialSerializer,JobSerializer,ApplicationSerializer,InterviewSheduleSerializer
from Tpoapi.models import Student,Company,TPO,Materials,Job,Application,InterviewSchedule

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class TpoCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=TpoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Tpo")
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
      

class StudentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = StudentSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Student.objects.all()
        serializer=StudentSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Student.objects.get(id=id)
        serializer=StudentSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    # def update(self,request,*args,**kwargs):
    #     serializer=StudentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    
    
class MaterialsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=MaterialSerializer(data=request.data)
        tpo_id=request.user.id
        tpo_obj=TPO.objects.get(id=tpo_id)
        if tpo_obj.user_type=="Tpo":
            if serializer.is_valid():
                serializer.save()
                return Response(data={'status':1,'data':serializer.data})
            else:
                error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
                return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response(request,data={'status':0,'msg':"Permission Denied for current user"})
   
        
        
    def list(self,request,*args,**kwargs):
        qs=Materials.objects.all()
        serializer=MaterialSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Materials.objects.get(id=id)
        serializer=MaterialSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = Materials.objects.get(id=id)
            instance.delete()
            return Response(data={'status':1,'msg':"material removed"})

        except Materials.DoesNotExist:
            return Response(data={'status':0,"msg": "material not found"}, status=status.HTTP_404_NOT_FOUND)
        


class ApplicationView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=Application.objects.all()
        serializer=ApplicationSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Application.objects.get(id=id)
        serializer=ApplicationSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    @action(methods=["post"],detail=True)
    def accept_application(self, request, *args, **kwargs):
        apply_id = kwargs.get("pk")
        try:
            apply_obj = Application.objects.get(id=apply_id)
        except Application.DoesNotExist:
            return Response(data={'status':0,"msg": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        apply_obj.status = "APPROVED"
        apply_obj.save()
        return Response(data={'status':1,"msg": "Application accepted successfully"}, status=status.HTTP_200_OK)
    
    
    @action(methods=["post"],detail=True)
    def reject_application(self, request, *args, **kwargs):
        apply_id = kwargs.get("pk")
        try:
            apply_obj = Application.objects.get(id=apply_id)
        except Application.DoesNotExist:
            return Response(data={'status':0,"msg": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        apply_obj.status = "REJECTED"
        apply_obj.save()
        return Response(data={'status':1,"msg": "Application rejected successfully"}, status=status.HTTP_200_OK)


class InterviewSheduleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=InterviewSchedule.objects.all()
        serializer=InterviewSheduleSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=InterviewSchedule.objects.get(id=id)
        serializer=InterviewSheduleSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
