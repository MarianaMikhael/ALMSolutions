from django.shortcuts import render, redirect
from .models.fornecedores import t_fornecedor
from .models.clientes import t_cliente
from .forms.forms import fornecedorForm, clienteForm




def fornecedores(request):
    fornecedores = t_fornecedor.objects.all()
    form = fornecedorForm(request.POST or None)
    
    if 'criar' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    
    if 'apagar' in request.GET:
        id = request.GET.get('id_fornecedor')
        fornecedor = t_fornecedor.objects.get(id_fornecedor=id)
        fornecedor.delete()

        return redirect('fornecedores')

    return render(request, 'calendario/fornecedores/fornecedores.html', {'fornecedores':fornecedores, 'form': form})

    
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


def clientes(request):
    clientes = t_cliente.objects.all()
    form = clienteForm(request.POST or None)
    
    if 'criar' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('clientes')

    if 'apagar' in request.GET:
        id = request.GET.get('id_cliente')
        cliente = t_cliente.objects.get(id_cliente=id)
        cliente.delete()

        return redirect('clientes')

    return render(request, 'calendario/clientes/clientes.html', {'clientes':clientes, 'form': form})

    
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
