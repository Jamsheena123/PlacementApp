from django.urls import path
from companyapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()



urlpatterns=[
    path("signup/",views.CompanyCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),


] +router.urls