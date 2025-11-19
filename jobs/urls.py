from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndustryViewset, LocationViewset, CompanyViewset, PostJobViewset, AvailableJobsViewset

router = DefaultRouter()
router.register(r'industries', IndustryViewset, basename='industries')
router.register(r'locations', LocationViewset, basename='locations')
router.register(r'companies', CompanyViewset, basename='companies')
router.register(r'postjobs', PostJobViewset, basename='postjobs')
router.register(r'availablejobs', AvailableJobsViewset, basename='availablejobs')

urlpatterns = [
    path('api/', include(router.urls)),
]