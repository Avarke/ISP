from django.urls import path
from . import views

app_name="knygynas"

urlpatterns = [
    
    path("", views.IndexView.as_view(), name="index"),
    path("prisijungti/", views.LoginView.as_view(), name="login"),
    path("vartotojas/", views.VartotojasView.as_view(), name="vartotojas"),
    path("redaguoti-vartotoja/", views.RedaguotiVartotoja.as_view(), name="redaguoti-vartotoja"),
    path("istrinti-vartotoja/", views.IstrintiVartotoja.as_view(), name="istrinti-vartotoja"),
    path("pakeisti-slaptazodi/", views.PakeistiSlaptazodi.as_view(), name="pakeisti-slaptazodi"),
    path("krepselis/", views.Krepselis.as_view(), name="krepselis"),
    path("apmokejimas/", views.Apmokejimas.as_view(), name="apmokejimas"),
    path("registracija/", views.Registracija.as_view(), name="sign-up"),
    
    
    
    # path("", views.home, name="home"),
    # path("todos/", views.todos, name="todos")
]

