from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplyJobViewset, MyApplicationHistoryViewset, JobApplicationsHistoryViewset

router = DefaultRouter()
router.register(r'apply-job', ApplyJobViewset, basename='apply-job')
router.register(r'my-applications-history', MyApplicationHistoryViewset, basename='my-applications')
router.register(r'job-applications-history', JobApplicationsHistoryViewset, basename='job-applications')

urlpatterns = [
    path('api/', include(router.urls)),
]