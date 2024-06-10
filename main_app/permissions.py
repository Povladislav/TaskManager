from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin_worker"


class IsWorkerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("worker", "admin_worker")


class IsWorkerOrAdminOrCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("worker", "admin_worker", "customer")


class IsAssignee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "worker"


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "customer"
