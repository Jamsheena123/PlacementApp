from django.urls import path
from studentapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()




urlpatterns=[
    path("signup/",views.StudentCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("profile/",views.StudentProfileView.as_view(),name="student_profile"),




] +router.urls