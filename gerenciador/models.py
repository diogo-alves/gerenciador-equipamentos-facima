#encoding:utf-8

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.

class Local(models.Model):
    nome = models.CharField(max_length=80)

    class Meta:
        db_table = 'local'
        verbose_name = 'Local de instalação'
        verbose_name_plural = 'Locais de instalação'

    def __unicode__(self):
        return self.nome

class Usuario(models.Model):

    TIPO_USUARIO = (
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        (u'funcionário', u'Funcionário'),
        ('outro', 'Outro')
    )

    nome = models.CharField(max_length=80)
    tipo = models.CharField(u'tipo de usuário', max_length=40, choices=TIPO_USUARIO, default=1);
    telefone = models.CharField(max_length=12)
    email = models.CharField(max_length=40)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuário'
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome


class Equipamento(models.Model):

    TIPO_EQUIPAMENTO = (
        (1, u'Áudiovisual'),
        (2, u'Informática'),
        (3, 'Outro')
        )

    ESTADO_EQUIPAMENTO = (
        ('funcionando', 'Funcionando'),
        (u'manutenção', u'Em manutenção'),
        ('danificado', 'Danificado'),
        ('outro', 'Outro')
    )

    numero = models.IntegerField(u'número', max_length=3, primary_key=True)
    descricao = models.CharField(u'descrição', max_length=80, null=False)
    tipo = models.IntegerField('tipo de equipamento', choices=TIPO_EQUIPAMENTO, max_length=1, default=2)
    serial = models.CharField(u'número de série', max_length=40, blank=True)
    disponivel = models.BooleanField(u'disponível', default=True)
    estado =  models.CharField('estado do equipamento', max_length=40, choices=ESTADO_EQUIPAMENTO, default=1)
    observacao = models.TextField(u'Observação', max_length=300, blank=True)

    class Meta:
        db_table = 'equipamento'

    def __unicode__(self):
        return '%s %s - %s' % (u'cód.', self.numero, self.descricao)


class Emprestimo(models.Model):
    usuario = models.ForeignKey(Usuario, verbose_name=u'usuário')
    equipamento = models.ManyToManyField(Equipamento, limit_choices_to = {'disponivel':True, 'estado': 'funcionando'}, verbose_name=u'equipamentos')
    funcionario_emprestimo = models.ForeignKey(User, related_name="%(class)s_emprestimo", null=True, blank=True, verbose_name=u'Inspetor')
    local_uso = models.ForeignKey(Local, verbose_name=u'Instalação')
    data_emprestimo = models.DateTimeField(u'data de empréstimo', default=datetime.now)
    prazo_devolucao = models.DateTimeField(u'prazo para devolução')
    devolvido = models.BooleanField(default=False)
    data_devolucao = models.DateTimeField(u'data da devolução', null=True)
    funcionario_devolucao = models.ForeignKey(User, related_name="%(class)s_devolucao", null=True, blank=True, verbose_name=u'Inspetor')

    class Meta:
            db_table = 'emprestimo'
            verbose_name = u'empréstimo'
            ordering = ('-data_emprestimo', )

    def equipamento_emprestado(self):
        return ' + '.join([obj.descricao for obj in self.equipamento.all()])
    equipamento_emprestado.short_description = 'Equipamento'

    def __unicode__(self):
        return u'%s - %s' %(self.usuario, self.equipamento_emprestado())
