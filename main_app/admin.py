from django.contrib import admin

from main_app.models import Task


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
