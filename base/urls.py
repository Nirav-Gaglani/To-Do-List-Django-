from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.TaskLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegistrationPage.as_view(), name='registration-page'),

    path('', views.TaskList.as_view(), name='tasks',),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name ='detail_view'),
    path('create-task/', views.CreateTask.as_view(), name='create-task'),
    path('update-task/<int:pk>/', views.UpdateTask.as_view(), name = 'update-task'),
    path('delete-task/<int:pk>/', views.DeleteTask.as_view(), name='delete-task'),
]