from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ApplyJobSerializer, ApplicantHistorySerializer, EmployerApplicationSerializer
from .models import ApplicationHistory, ApplyJob
from .permissions import IsAuthenticatedToApply, IsApplicantOwner, IsJobOwner
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ApplyJobViewset(viewsets.ModelViewSet):
    # Only authenticated users can apply for jobs (POST)
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobSerializer
    permission_classes = [IsAuthenticatedToApply]
    http_method_names = ['post']

    def perform_create(self, serializer):
        # Automatically set the applicant to the logged-in user
        serializer.save(applicant=self.request.user)

# For Job Seekers - "My Applications"
class MyApplicationHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """
    For Job Seekers - "My Applications"
    - Only authenticated users can access
    - Users can only see their own applications
    """
    serializer_class = ApplicantHistorySerializer
    permission_classes = [IsAuthenticated, IsApplicantOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ApplyJob.objects.none()
        
        return ApplyJob.objects.filter(
            applicant=self.request.user
        ).select_related('job', 'job__company').order_by('applied_on')


# For Employers - "Applications to My Jobs"
class JobApplicationsHistoryViewset(viewsets.ModelViewSet):
    """
    For Employers - "Applications to My Jobs"
    - Only authenticated users can access
    - Employers can only see applications to jobs they posted
    - Employers can update application status obly
    """
    serializer_class = EmployerApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobOwner]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ApplyJob.objects.none()
        
        return ApplyJob.objects.filter(
            job__posted_by=self.request.user
        ).select_related('job', 'applicant').order_by('-applied_on')

    def perform_update(self, serializer):
        # Automatically set reviewed_by and reviewed_at when status is updated
        from django.utils import timezone
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now()
        )