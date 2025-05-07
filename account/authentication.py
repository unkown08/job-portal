from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return super().authenticate(request)
    
from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    message = "Only recruiters are allowed to perform this action"
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'recruiter')