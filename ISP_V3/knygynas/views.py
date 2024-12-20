from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import Knyga
from django.views.generic import TemplateView

# Create your views here.
# def home(request):
#     return render(request, "home.html")

# def todos(request):
#     items = TodoItem.objects.all()
#     return render(request, "todos.html", {"todos": items})

class IndexView(generic.ListView):
    template_name = "knygynas/index.html"
    context_object_name = "all_books"  # Updated to match the template context

    def get_queryset(self):
        # Return all books from the Knyga model
        return Knyga.objects.all()
    
class LoginView(TemplateView):
    template_name = "knygynas/prisijungimas.html"
    
class VartotojasView(TemplateView):
    template_name = "knygynas/vartotojas.html"

class RedaguotiVartotoja(TemplateView):
    template_name = "knygynas/redaguoti-vartotoja.html"


class IstrintiVartotoja(TemplateView):
    template_name = "knygynas/istrinti-vartotoja.html"


class PakeistiSlaptazodi(TemplateView):
    template_name = "knygynas/pakeisti-slaptazodi.html"



class Krepselis(TemplateView):
    template_name = "knygynas/krepselis.html"


class Apmokejimas(TemplateView):
    template_name = "knygynas/apmokejimas.html"



class Registracija(TemplateView):
    template_name = "knygynas/registracija.html"

