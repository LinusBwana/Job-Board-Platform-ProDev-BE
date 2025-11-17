from rest_framework.permissions import BasePermission

class IsAuthenticatedToApply(BasePermission):
    """
    Only authenticated users can create applications (POST)
    Must be logged in to apply for jobs
    """
    def has_permission(self, request, view):
        # Only allow POST method and only for authenticated users and their rols is Job Seeker
        if request.method == 'POST':
            return (
                request.user and request.user.is_authenticated 
                and request.user.role == 'job_seeker')
        
        # Deny all other methods (GET, PUT, PATCH, DELETE)
        return False

class IsApplicantOwner(BasePermission):
    """
    Allows applicants to see their own application history
    """
    def has_permission(self, request, view):
        # User must be authenticated
        return (
            request.user and request.user.is_authenticated 
            and request.user.role == 'job_seeker'
            )

    def has_object_permission(self, request, view, obj):
        # Only the applicant can view their own application
        return obj.applicant == request.user

class IsJobOwner(BasePermission):
    """
    Only allow employers to see applications to their own jobs
    Only job owners can update application status
    """
    def has_permission(self, request, view):
        # User must be authenticated
        return (
            request.user and request.user.is_authenticated 
            and request.user.role == 'employer'
            )
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the one who posted the job
        return obj.job.posted_by == request.user