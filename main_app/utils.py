from main_app.models import Task


def get_tasks_for_user(user):
    if user.role == 'worker':
        return Task.objects.filter(worker=user) | Task.objects.filter(worker__isnull=True)
    elif user.role == 'customer':
        return Task.objects.filter(client=user)
    return Task.objects.none()


def assign_worker_to_task(task_id, worker):
    try:
        task = Task.objects.get(pk=task_id, status=Task.Statuses.WAITING_FOR_WORKER)
        task.worker = worker
        task.status = Task.Statuses.PROCESSING
        task.save()
        return {"success": "Task assigned"}, 200
    except Task.DoesNotExist:
        return {"error": "Task not found or already assigned"}, 404


def complete_task(task_id, worker, report):
    try:
        task = Task.objects.get(pk=task_id, worker=worker, status=Task.Statuses.PROCESSING)
        task.status = Task.Statuses.DONE
        task.report = report
        task.save()
        return {"success": "Task completed"}, 200
    except Task.DoesNotExist:
        return {"error": "Task not found or not in processing state"}, 404

