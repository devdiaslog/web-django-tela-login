from django.shortcuts import render
from django.shortcuts import redirect
from .models import Usuarios
from hashlib import sha256
from django.http.response import HttpResponse


def validar_register(request):
  nome = request.POST.get('nome')
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  
  if len(nome.strip()) == 0 or len(email.strip()) == 0:
    return redirect("/auth/register/?status=0")
    # Se o usuário não digitou nada
  if len(senha)<8:
    return redirect("/auth/register/?status=1")
    # Se o usuário preencheu nome e email porém a senha é menor que 8
  usuario = Usuarios.objects.filter(email=email)
  if len(usuario) > 0:
    return redirect("/auth/register/?status=2")
    #Se o usuario já é cadastrado
  
  # Caso não tenha erro, cadastrar no banco de dados
  try:
    senha = sha256(senha.encode()).hexdigest()
    usuario = Usuarios(nome=nome,email=email,senha=senha)
    usuario.save()
    return redirect("/auth/register/?status=3")
    # Deu tudo ta certo
  except:
    return redirect("/auth/register/?status=4")
    # Erro interno do sistema

def validar_login(request):
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  senha = sha256(senha.encode()).hexdigest()
  usuario = Usuarios.objects.filter(email=email).filter(senha=senha)
  if len(usuario) > 0:
    request.session['usuario_logado'] = True
    return redirect("/auth/usuarios/")
  else:
    return redirect("/auth/login/?status=0")
    #Usuario ou senha incorreto

def logout(request):
  return HttpResponse(request.session.get_expiry_date())
  # request.session.flush()
  # return redirect("/auth/login/")
  
def login(request):
  status = request.GET.get("status")
  return render(request,"login.html",{"status":status})

def register(request):
  status = request.GET.get('status')
  return render(request,"register.html",{"status":status})

def index(request):
  if request.session.get('usuario_logado'):
    usuarios = Usuarios.objects.all()
    return render(request,"lista_usuarios.html",{"usuarios":usuarios})
  return redirect("/auth/login/?status=1")