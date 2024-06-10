from django.urls import path

from main_app.views import CompleteTaskView, TaskView, WorkerTaskView

urlpatterns = [
    path("tasks/", TaskView.as_view(), name='create-task'),
    path("tasks/<int:pk>/assign_worker/", WorkerTaskView.as_view(), name='assign-worker'),
    path("tasks/complete_task/<int:pk>/", CompleteTaskView.as_view(), name='complete-task'),
]
