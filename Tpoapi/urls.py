from django.urls import path
from Tpoapi import views
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("student",views.StudentView,basename="student_list"),
router.register("company",views.CompanyView,basename="company_list"),
router.register("material",views.MaterialsView,basename="materials"),
router.register("application",views.ApplicationView,basename="application"),
router.register("scheduledinterview",views.InterviewSheduleView,basename="scheduledinterview"),
router.register("quiz",views.QuizView,basename="quiz"),


urlpatterns=[
    path("register/",views.TpoCreationView.as_view(),name="signin"),
    path('token/',views.CustomAuthToken.as_view(), name='token'),


] +router.urls