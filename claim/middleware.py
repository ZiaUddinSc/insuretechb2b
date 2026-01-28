# middleware.py
import threading
from django.utils.deprecation import MiddlewareMixin

_user = threading.local()

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _user.value = request.user

def get_current_user():
    return getattr(_user, "value", None)
