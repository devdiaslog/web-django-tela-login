from django.contrib import admin
from .models import Usuarios

@admin.register(Usuarios)
class AdminUsuario(admin.ModelAdmin):
  list_display = ('nome','email')
