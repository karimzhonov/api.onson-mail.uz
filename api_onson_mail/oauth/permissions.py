from rest_framework.permissions import BasePermission


class HasDjangoPermission(BasePermission):

    def has_permission(self, request, view):
        print(request.method)
        method_dict = {
            'GET': 'view',
            'HEAD': 'view',
            'OPTIONS': 'view',
            'PATCH': 'change',
            'POST': 'add',
            'PUT': 'change',
            'DELETE': 'delete',
        }
        if getattr(view, 'perms', False):
            perms = []
            for perm in view.perms:
                app, model = perm.split('.')
                perms.append(''.join((app, '.', method_dict[request.method], "_", model)))
            return request.user.has_perms(perms)
        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
