from rest_framework import serializers

from authentication.models import User
from main_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class AssignWorkerSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()

    def validate_worker_id(self, value):
        try:
            worker = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Worker does not exist")
        if worker.role not in ["worker", "admin_worker"]:
            raise serializers.ValidationError("User is not a worker or admin_worker")
        return value

    def update(self, instance, validated_data):
        worker_id = validated_data.get('worker_id')
        instance.worker_id = worker_id
        instance.status = Task.Statuses.PROCESSING
        instance.save()
        return instance


class CompleteTaskSerializer(serializers.ModelSerializer):
    report = serializers.CharField()

    class Meta:
        model = Task
        fields = ['report']
