from django.shortcuts import render, redirect
from .models.fornecedores import t_fornecedor
from .models.clientes import t_cliente
from .forms.forms import fornecedorForm, clienteForm




def fornecedores(request):
    fornecedores = t_fornecedor.objects.all()
    return render(request, 'calendario/fornecedores/fornecedores.html', {'fornecedores':fornecedores})

def cadastrofornecedor(request):
    form = fornecedorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('fornecedores')

    return render(request, 'calendario/fornecedores/cadastrofornecedores.html', {'form':form})


def atualizafornecedor(request, id):
    fornecedor = t_fornecedor.objects.get(id_fornecedor=id)
    form = fornecedorForm(request.POST or None, instance=fornecedor)

    if form.is_valid():
        form.save()
        return redirect('fornecedores')

    return render(request, 'calendario/fornecedores/cadastrofornecedores.html', {'form':form, 'fornecedor': fornecedor})


def apagarfornecedor(request, id):
    fornecedor = t_fornecedor.objects.get(id_fornecedor=id)

    if request.method == "POST":
        fornecedor.delete()
        return redirect('fornecedores')

    return render(request, 'calendario/fornecedores/apagarfornecedor.html', {'fornecedor':fornecedor})



def clientes(request):
    clientes = t_cliente.objects.all()
    return render(request, 'calendario/clientes/clientes.html', {'clientes':clientes})

    
def cadastrocliente(request):
    form = clienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('clientes')

    return render(request, 'calendario/clientes/cadastroclientes.html', {'form':form})


def atualizacliente(request, id):
    cliente = t_cliente.objects.get(id_cliente=id)
    form = clienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        return redirect('clientes')

    return render(request, 'calendario/clientes/cadastroclientes.html', {'form':form, 'cliente': cliente})


def apagarcliente(request, id):
    cliente = t_cliente.objects.get(id_cliente=id)

    if request.method == "POST":
        cliente.delete()
        return redirect('clientes')

    return render(request, 'calendario/clientes/apagarcliente.html', {'cliente':cliente})
