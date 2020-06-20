from django.contrib import admin

# Register your models here.

from calendario.models import clientes, fornecedores

admin.site.register(clientes.t_cliente),
admin.site.register(fornecedores.t_fornecedor),
