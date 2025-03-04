from rest_framework.permissions import BasePermission


class CompanyPermission(BasePermission):

    def has_permission(self, request, view):
        if not view.kwargs.get('company_sub'):
            return True
        return request.user.companies.filter(sub=view.kwargs['company_sub']).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
