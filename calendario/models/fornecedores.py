from django.db import models

# Create your models here.

import re
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class t_fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome = models.CharField(_('Nome'), max_length=30,
        null=False, blank=False)
    sobrenome = models.CharField(_('Sobrenome'), max_length=30,
        null=False, blank=False)
    email = models.EmailField(_('E-mail'), max_length=255,
        unique=True, null=False, blank=False, validators=[
            validators.RegexValidator(re.compile(
                '^[\w.@+-]+$'),
                _('Insira um endereço de e-mail válido!'),
                _('Inválido!'))],
                             )
    celular = models.CharField(_('Celular'), max_length=20, unique=True)

    class Meta:
        verbose_name = _('Fornecedor')
        verbose_name_plural = _('Fornecedores')

    def get_full_name(self):
        nome_completo = '%s %s' % (self.nome, self.sobrenome)
        return nome_completo.strip()

    def get_short_name(self):
        return self.nome

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
    
    def __str__(self):
        return self.get_full_name()
