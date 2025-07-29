from django.shortcuts import render
from django.views.generic import TemplateView

# from common.utils import get_organizer


# Create your views here.
class HomePage(TemplateView):
    template_name = 'home.html'
