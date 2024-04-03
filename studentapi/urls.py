from django.urls import path
from studentapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("companies",views.CompanyView,basename="company_list"),
router.register("jobs",views.jobView,basename="job_list"),
router.register("applicationstatus",views.ApplicationStatusView,basename="applicationstatus"),
router.register("interviews",views.InterviewView,basename="interview_list"),
router.register("materials",views.MaterialView,basename="materials_list"),
router.register("quiz",views.QuizView,basename="quiz"),


urlpatterns=[
    path("signup/",views.StudentCreationView.as_view(),name="signup"),
    path('token/',views.CustomAuthToken.as_view(), name='token'),
    path("profile/",views.StudentProfileView.as_view(),name="student_profile"),




] +router.urls