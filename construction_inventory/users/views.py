from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from .models import CustomUser

class CustomLoginView(LoginView):
    template_name = 'users/registration/login.html'
    redirect_authenticated_user = True

class ProfileSettings(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_settings.html'