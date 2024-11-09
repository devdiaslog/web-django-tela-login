from django.urls import path
from .views import login,register,validar_register,validar_login,index,logout

urlpatterns = [
  path("login/",login,name="login"),
  path("register/",register,name="register"),
  path("usuarios/",index,name="usuarios"),
  path("logout/",logout,name="logout"),
  path("validar_register/",validar_register,name="validar_register"),
  path("validar_login/",validar_login,name="validar_login"),
]