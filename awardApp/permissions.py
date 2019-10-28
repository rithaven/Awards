# from rest_framework.permissions import SAFE_METHODS,BasePermissions

# class IsAdminOrReadOnly(BasePermissions):
#   def has_permission(self,request,view):
#     if request.method in SAFE_METHODS:
#          return True
#     else:
#       return request.user.is_staff