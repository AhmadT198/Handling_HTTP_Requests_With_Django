from django.urls import path

from users.views import SingleStudent, MultipleStudents

urlpatterns = [
    path('', MultipleStudents.as_view()),
    path('<int:id>', SingleStudent.as_view())

]