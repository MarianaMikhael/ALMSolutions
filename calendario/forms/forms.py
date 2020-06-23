from django.forms import ModelForm
from django import forms

from calendario import models as m


class clienteForm(ModelForm):
    class Meta:
        model = m.clientes.t_cliente
        exclude = [
            'id_cliente',
        ]


class fornecedorForm(ModelForm):
    class Meta:
        model = m.fornecedores.t_fornecedor
        exclude = [
            'id_fornecedor',
        ]

'''
class eventoForm(forms.ModelForm):
    class Meta:
        model = m.eventos.t_evento
        exclude = [
            'id_evento',
            # 'data_hora',
        ]

    def __init__(self, *args, **kwargs):
        super(eventoForm, self).__init__(*args, **kwargs)
        self.fields['opcao_servico'].widget = forms.CheckboxSelectMultiple()
'''