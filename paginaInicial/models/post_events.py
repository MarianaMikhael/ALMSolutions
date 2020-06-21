import re

from django.db import models
from datetime import datetime
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from calendario.models import fornecedores


class Post(models.Model):
    tipo_evento = (
        ('Aniversario', 'Aniversário'),
        ('Casamento', 'Casamento'),
        ('Confrat', 'Confraternização'),
        ('Debutante', 'Debutante'),
        ('Locacao', 'Locação do Espaço'),
        ('Outros', 'Outros'),
    )

    opcao_servico = [
        ('Escolha o(s) serviço(s) a ser(em) incluídos: ', (
            ('Som / Ilum / Telao', 'Som / Iluminação / Telão'),
            ('Decoracao', 'Decoração'),
            ('Buffet', 'Buffet'),
            ('Outros', 'Outros'),
            )
        ),
    ]

    opcao_status = (
        ('', 'Aguardando Confirmação de Contrato'),
        ('', 'Cancelado'),
        ('', 'Contrato Confirmado'),
        ('', 'Realizado'),
    )

    uidd = models.CharField("Event ID", max_length=100, null=True, default='N/A')  # event id from google calendar
    summary = models.CharField("Título", max_length=500, null=True)
    start = models.DateTimeField("De", default=datetime.now, null=True)  # start event date
    end = models.DateTimeField("Até", default=datetime.now, null=True)  # end event date default=datetime.now
    location = models.CharField("Localização", max_length=500, null=True)
    description = models.CharField("Descrição(ões) Adicional(ais)", max_length=500, null=True)
    email = models.EmailField(_('Convidado'), max_length=255,
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Insira um e-mail válido.'),
            _('invalid'))], null=False, blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, blank=False,
        verbose_name='Valor Total do Evento')
    # fk_Fornecedor = models.ManyToManyField(fornecedores.t_fornecedor, blank=False,
    #     verbose_name="Fornecedor")

    def __str__(self):
        return self.summary
