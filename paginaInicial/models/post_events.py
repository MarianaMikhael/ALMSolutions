import re

from django.db import models
from datetime import datetime
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from calendario.models import fornecedores


class Post(models.Model):
    uidd = models.CharField("Event ID", max_length=500, null=True, default='N/A')  # event id from google calendar
    summary = models.CharField("Título", max_length=500, null=True)
    start = models.DateTimeField("De", default=datetime.now, null=True)  # start event date
    end = models.DateTimeField("Até", default=datetime.now, null=True)  # end event date default=datetime.now
    location = models.CharField("Localização", max_length=500, blank=True, null=True)
    description = models.TextField("Descrição(ões) Adicional(ais)", max_length=500, blank=True, null=True)
    email = models.EmailField(_('Convidado'), max_length=255,
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Insira um e-mail válido.'),
            _('invalid'))], null=False, blank=False)
    # fk_Fornecedor = models.ManyToManyField(fornecedores.t_fornecedor, blank=False,
    #     verbose_name="Fornecedor")
