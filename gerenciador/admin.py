#encoding:utf-8

from django.contrib import admin, messages
from gerenciador.models import *
from gerenciador.forms import UsuarioForm
from datetime import datetime
from django.utils.timezone import utc
from django.shortcuts import  render_to_response
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.middleware import csrf

class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = list_display
    list_per_page = 20

class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm
    list_display = ('nome', 'tipo', 'telefone', 'email',)
    list_display_links = list_display
    list_filter = ('tipo', )
    search_fields = ('nome','tipo')
    list_per_page = 20
    actions = ('ver_emprestimos_usuario',)

    def ver_emprestimos_usuario(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Selecione apenas um usuario por vez!')
        else:
            return HttpResponseRedirect("/admin/gerenciador/historico/usuario/%s" % queryset[0].id)

    ver_emprestimos_usuario.short_description = "Ver histórico de empréstimos do usuário"



class EquipamentoAdmin(admin.ModelAdmin):
    fields = ('numero', 'descricao', 'tipo', 'serial', 'estado', 'disponivel', 'observacao',)
    list_display = ('numero', 'descricao', 'tipo', 'serial', 'estado', 'disponivel', 'observacao',)
    list_display_links = list_display
    list_filter = ('tipo', 'estado', 'disponivel')
    search_fields = ('numero', 'descricao', 'serial',)
    list_per_page = 20
    actions = ('ver_emprestimos_equipamento',)

    def ver_emprestimos_equipamento(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Selecione apenas um equipamento por vez!')
        else:
            return HttpResponseRedirect("/admin/gerenciador/historico/equipamento/%s" % queryset[0].numero)

    ver_emprestimos_equipamento.short_description = "Ver histórico de empréstimos do equipamento"


class EmprestimoAdmin(admin.ModelAdmin):
    fields = ('usuario', 'equipamento', 'local_uso', 'prazo_devolucao')
    list_display = ('id', 'usuario', 'equipamento_emprestado', 'local_uso', 'funcionario_emprestimo', 'data_emprestimo', 'prazo_devolucao', 'devolvido', 'data_devolucao', 'funcionario_devolucao')
    list_display_links = list_display
   # list_filter = ('usuario', 'devolvido', 'data_emprestimo', 'prazo_devolucao', 'data_devolucao')
    search_fields = ('id', 'usuario',)
    filter_horizontal = ('equipamento',)
    list_per_page = 20
    actions = ('devolver_emprestimo', 'gerar_comprovante')

    def devolver_emprestimo(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, "Só é possível efetuar uma devolução por vez. Tente novamente!")
        elif len(Emprestimo.objects.filter(id__in = queryset).filter(devolvido = 'True')) > 0:
            messages.error(request, "O empréstimo já foi devolvido!")
        else:
            if 'post' in request.POST:
                Equipamento.objects.filter(emprestimo__in = queryset).update(disponivel = True)
                queryset.update(devolvido='True', data_devolucao = datetime .utcnow() . replace(tzinfo = utc), funcionario_devolucao = request.user)

                self.message_user(request, "Devolução realizada com sucesso!")
                # Return to the list page
                return HttpResponseRedirect(request.get_full_path())

            return render_to_response('devolucao_emprestimo.html',
                    {'equipamentos': Equipamento.objects.filter(emprestimo__in = queryset),
                     'queryset': queryset, 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                     'csrf_token': csrf.get_token(request)})

    devolver_emprestimo.short_description = "Devolver empréstimo selecionado"

    def gerar_comprovante(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro ao gerar o comprovante. Selecione apenas um empréstimo por vez!')
        else:
            return HttpResponseRedirect("/admin/comprovante/emprestimo/%s" % queryset[0].id)

    gerar_comprovante.short_description = "Gerar comprovante de empréstimo"

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'funcionario_emprestimo' , None ) is None :
            obj.funcionario_emprestimo = request.user
            obj.save()
        model = form.save()
        for equip in model.equipamento.all():
            equip.disponivel = False
            equip.save()

admin.site.register(Local, LocalAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Equipamento, EquipamentoAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)


