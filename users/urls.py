from django.urls import path

from users.views import *

urlpatterns = [

    path('students', MultipleStudents.as_view(), name="student-list"),
    path('students/<int:pk>', SingleStudent.as_view(), name="student-detail"),

    path('parents', MultipleParents.as_view(), name="parent-list"),
    path('parents/<int:pk>', SingleParent.as_view(), name="parent-detail"),

    path('subjects', MultipleSubjects.as_view(), name="subject-list"),
    path('subjects/<int:pk>', SingleSubject.as_view(), name="subject-detail"),

    path('modify/<int:studentID>/<int:subjectID>', ModifySubjects.as_view()),

    path('register', Register.as_view(), name="accounts-detail"),
    path('login', login.as_view()),
    path('logout', Logout.as_view())
]
