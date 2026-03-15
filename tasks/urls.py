from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/complete/', views.mark_task_completed, name='mark_task_completed'),
    path('subtasks/', views.subtask_list, name='subtask_list'),
    path('notes/', views.note_list, name='note_list'),
    path('categories/', views.category_list, name='category_list'),
]