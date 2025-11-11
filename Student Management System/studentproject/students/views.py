# students/views.py
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

# lazy import of firebase client
from studentproject.firebase import get_firestore

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'age', 'course']
    ordering_fields = ['created_at', 'name', 'age']

    def _student_to_dict(self, student):
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "course": student.course,
            "created_at": student.created_at.isoformat() if getattr(student, "created_at", None) else None,
            "updated_at": student.updated_at.isoformat() if getattr(student, "updated_at", None) else None,
        }

    def perform_create(self, serializer):
        student = serializer.save()  # Save to MySQL first
        try:
            db = get_firestore()
            if db:
                db.collection('students').document(str(student.id)).set(self._student_to_dict(student))
        except Exception as e:
            print("Firebase create error:", e)

    def perform_update(self, serializer):
        student = serializer.save()
        try:
            db = get_firestore()
            if db:
                db.collection('students').document(str(student.id)).set(self._student_to_dict(student), merge=True)
        except Exception as e:
            print("Firebase update error:", e)

    def perform_destroy(self, instance):
        student_id = instance.id
        instance.delete()
        try:
            db = get_firestore()
            if db:
                db.collection('students').document(str(student_id)).delete()
        except Exception as e:
            print("Firebase delete error:", e)
