from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView


# from common.utils import get_organizer


# Create your views here.
class HomePage(TemplateView):
    template_name = 'home.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
