#encoding:utf-8

from django.conf.urls import patterns, include, url
from gerenciador.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'facima.views.home', name='home'),
    # url(r'^facima/', include('facima.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', index),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/comprovante/emprestimo/(?P<pk>\d+)', comprovante),
    url(r'^admin/gerenciador/historico/usuario/(?P<pk>\d+)', buscar_historico_usuario),
    url(r'^admin/gerenciador/historico/equipamento/(?P<pk>\d+)', buscar_historico_equipamento),
)
