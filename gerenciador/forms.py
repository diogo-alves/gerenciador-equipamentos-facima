#encoding: utf-8

from  django.contrib.localflavor.br.forms import BRPhoneNumberField
from django.forms import  ModelForm
from gerenciador.models import Usuario


class UsuarioForm(ModelForm):
    telefone = BRPhoneNumberField(label='Telefone', help_text=u'Digite um número válido no formato xx-xxxx-xxxx.')

    class Meta:
        model = Usuario