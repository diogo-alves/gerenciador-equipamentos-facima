#encoding:utf-8

from gerenciador.models import *
from django.shortcuts import render_to_response

# Create your views here.

def index(request):
    return render_to_response('index.html')


def comprovante(request, pk):
    try:
        emprestimo = Emprestimo.objects.get(id=pk)
    except Exception:
        return render_to_response('404.html')

    return render_to_response('comprovante_emprestimo.html', {'emprestimo': emprestimo, 'numero': pk})


def buscar_historico_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
        emprestimos = Usuario.objects.get(id=pk).emprestimo_set.order_by('-id')
    except Exception:
        return render_to_response('404.html')

    return render_to_response('historico_emprestimos_usuario.html',
            {'emprestimos': emprestimos, 'usuario': usuario})


def buscar_historico_equipamento(request, pk):
    try:
        equipamento = Equipamento.objects.get(numero=pk)
        emprestimos = Equipamento.objects.get(numero=pk).emprestimo_set.order_by('-id')
    except Exception:
        return render_to_response('404.html')

    return render_to_response('historico_emprestimos_equipamento.html',
            {'emprestimos': emprestimos, 'equipamento': equipamento})
