from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from companyapi.serializer import CompanySerializer,JobSerializer,ApplicationSerializer,InterviewSheduleSerializer
from Tpoapi.models import Student,Company,TPO,Materials,Job,Application,InterviewSchedule

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token




class CompanyCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Company")
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
        

class JobView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=JobSerializer(data=request.data)
        cmp_id=request.user.id
        cmp_obj=Company.objects.get(id=cmp_id)
        if serializer.is_valid():
            serializer.save(posted_by=cmp_obj)
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
  
            
    def list(self,request,*args,**kwargs):
        cmp_id=request.user.id
        cmp_obj=Company.objects.get(id=cmp_id)
        qs=Job.objects.filter(posted_by=cmp_obj)
        serializer=JobSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Job.objects.get(id=id)
        serializer=JobSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = Job.objects.get(id=id)
            instance.delete()
            return Response(data={'status':1,'data':'Job removed'})
        except Materials.DoesNotExist:
            return Response(data={'status':0,'msg':'Job not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ApplicationView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        cmp_id=request.user.id
        cmp_obj=Company.objects.get(id=cmp_id)
        qs=Application.objects.filter(job__posted_by=cmp_obj)
        serializer=ApplicationSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Application.objects.get(id=id)
        serializer=ApplicationSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    

    # @action(methods=["post"],detail=True)
    # def accept_application(self, request, *args, **kwargs):
    #     apply_id = kwargs.get("pk")
    #     try:
    #         apply_obj = Application.objects.get(id=apply_id)
    #     except Application.DoesNotExist:
    #         return Response({"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
    #     apply_obj.status = "APPROVED"
    #     apply_obj.save()
    #     return Response({"message": "Application accepted successfully"}, status=status.HTTP_200_OK)
    
    # @action(methods=["post"],detail=True)
    # def reject_application(self, request, *args, **kwargs):
    #     apply_id = kwargs.get("pk")
    #     try:
    #         apply_obj = Application.objects.get(id=apply_id)
    #     except Application.DoesNotExist:
    #         return Response({"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
    #     apply_obj.status = "REJECTED"
    #     apply_obj.save()
    #     return Response({"message": "Application rejected successfully"}, status=status.HTTP_200_OK)
    
    @action(methods=["post"],detail=True)
    def schedule_interview(self,request,*args,**kwargs):
        serializer=InterviewSheduleSerializer(data=request.data)
        company_id=request.user.id
        company_obj=Company.objects.get(id=company_id)
        appl_id=kwargs.get("pk")
        appl_obj=Application.objects.get(id=appl_id)
        if appl_obj.status!="APPROVED":
            return Response(request,data={'status':0,'msg':'application is not approved.. approve it first!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save(company=company_obj,application=appl_obj)
                return Response(data={'status':1,'data':serializer.data})
            else:
                error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
                return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)        
            
            
class InterviewSheduleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        cmp_id=request.user.id
        cmp_obj=Company.objects.get(id=cmp_id)
        qs=InterviewSchedule.objects.filter(company=cmp_obj)
        serializer=InterviewSheduleSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=InterviewSchedule.objects.get(id=id)
        serializer=InterviewSheduleSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
