from django.urls import path

from users.views import POST_GET, Update_Delete

urlpatterns = [
    path('', POST_GET),
    path('<int:id>', Update_Delete)

]