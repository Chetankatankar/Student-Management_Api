from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StudentViewSet

def home(request):  
    return HttpResponse("Welcome to Student API")

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', home),                          # home page route
    path('api/', include(router.urls)),       # api routes
]
