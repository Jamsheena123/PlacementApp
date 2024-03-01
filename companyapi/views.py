from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from companyapi.serializer import CompanySerializer


class CompanyCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Company")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
