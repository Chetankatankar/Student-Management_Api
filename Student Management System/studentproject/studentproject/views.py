# studentproject/views.py
from django.shortcuts import render

def home(request):
    # agar koi dynamic data bhejna ho to yahan context dict banake pass kar sakte ho
    context = {
        'project_name': 'Student Management System',
        'description': 'Welcome to Student API — manage students quickly and easily.',
    }
    return render(request, 'home.html', context)
