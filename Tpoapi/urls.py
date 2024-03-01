from django.urls import path
from Tpoapi import views
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("student",views.StudentView,basename="student_list"),
router.register("company",views.CompanycreateView,basename="company_list"),



urlpatterns=[
    path("register/",views.TpoCreationView.as_view(),name="signin"),
    path("token/",ObtainAuthToken.as_view(),name="token"),


] +router.urls