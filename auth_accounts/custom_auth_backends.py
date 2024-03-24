from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        user_model = get_user_model()
        
        if email:
            try:
                user = user_model.objects.get(email=email)
                if user.check_password(password):
                    return user
            except user_model.DoesNotExist:
                return None
        elif username:
            try:
                user = user_model.objects.get(username=username)
                if user.check_password(password):
                    return user
            except user_model.DoesNotExist:
                return None

        return None