from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main_app.models import Task
from main_app.permissions import (IsCustomer, IsWorkerOrAdmin,
                                  IsWorkerOrAdminOrCustomer)
from main_app.serializers import CompleteTaskSerializer, TaskSerializer
from main_app.utils import (assign_worker_to_task, complete_task,
                            get_tasks_for_user)


class TaskView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomer()]
        elif self.request.method == "GET":
            return [IsWorkerOrAdminOrCustomer()]
        return super().get_permissions()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        data = request.data.copy()
        data['client'] = request.user.id
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        tasks = get_tasks_for_user(request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class WorkerTaskView(generics.GenericAPIView):
    permission_classes = (IsWorkerOrAdmin,)
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        response_data, status_code = assign_worker_to_task(task_id, request.user)
        return Response(response_data, status=status_code)


class CompleteTaskView(generics.GenericAPIView):
    permission_classes = (IsWorkerOrAdmin,)
    serializer_class = CompleteTaskSerializer
    queryset = Task.objects.all()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        report = request.data.get('report')
        if not report:
            return Response({"error": "Report is required"}, status=400)
        response_data, status_code = complete_task(task_id, request.user, report)
        return Response(response_data, status=status_code)
