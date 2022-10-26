from django.urls import path

from users.views import *

urlpatterns = [

    path('students', MultipleStudents.as_view(), name="student-detail"),
    path('students/<int:pk>', SingleStudent.as_view(), name="student-detail"),

    path('parents', MultipleParents.as_view()),
    path('parents/<int:pk>', SingleParent.as_view()),

    path('subjects', MultipleSubjects.as_view(), name="subject-detail"),
    path('subjects/<int:pk>', SingleSubject.as_view(), name="subject-detail"),

    path('modify/<int:studentID>/<int:subjectID>', ModifySubjects.as_view()),

]
