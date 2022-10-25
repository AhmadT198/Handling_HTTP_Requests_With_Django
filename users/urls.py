from django.urls import path

from users.views import *

urlpatterns = [
    path('students', MultipleStudents.as_view()),
    path('students/<int:id>', SingleStudent.as_view()),

    path('parents', MultipleParents.as_view()),
    path('parents/<int:id>', SingleParent.as_view()),

    path('subjects', MultipleSubjects.as_view()),
    path('subjects/<int:id>', SingleSubject.as_view()),

    path('modify/<int:studentID>/<int:subjectID>', ModifySubjects.as_view()),

]
