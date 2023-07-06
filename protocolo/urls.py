from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "protocolo"

urlpatterns = [
                  path('', views.protocolos_view, name="protocols"),
                  path('incrementar/<int:part_id>/<int:participant_id>', views.incrementar, name='incrementar'), #estou só a fazer testes!
                  path('dashboard', views.dashboard_view, name="dashboard"),
                  path('popup',views.popup_view,name = 'popup'),
                  path('', views.menu_protocolo_view, name="app-view"),
                  #path('risk',views.risk_form_view,name="risk"),
                  path('teste', views.teste, name='teste'),
                  path('participant/<int:protocol_id>', views.participant_risk_view, name='participant_risk'),
                  path('protocol-participants/<int:protocol_id>', views.protocol_participants_view,
                       name="protocol-participants"),
                  path('participants', views.participants_view, name="participants"),
                  path('dashboard-content', views.dashboard_content_view, name="dashboard-content"),
                  path('atualizar-tabela', views.parte_do_utilizador_add_view, name = "atualizar-tabela"),
                  path('parts/<int:protocol_id>/<int:patient_id>', views.parts_view, name="parts"),
                  path('parte', views.parte_view, name = "parte"),
                  path('areas/<int:protocol_id>/<int:part_id>/<int:patient_id>', views.areas_view, name="areas"),
                  path('instruments/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:patient_id>',
                       views.instruments_view,
                       name="instruments"),
               #    path('risco', views.risco_view, name="risco"),
                  path('dimension/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:patient_id>',
                       views.dimensions_view, name="dimensions"),
                  path(
                      'section/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:dimension_id>/<int:patient_id>',
                      views.sections_view, name="sections"),
                  path(
                      'question/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:dimension_id>/<int:section_id>/<int:patient_id>',
                      views.question_view, name="question"),
                  path('nova_pagina_risk_report/',views.nova_pagina_risk_report, name='nova_pagina_risk_report'),
                  path('report/<int:resolution_id>', views.report_view, name="report"),
                  path('report_risk',views.report_risk,name="report_risk"), #estou só a fazer testes! A ver se este funciona
                  path('login', views.login_view, name="login"),
                  path('logout', views.logout_view, name="logout"),
                  path('profile/<int:participant_id>/', views.profile_view, name="participant"),
                  path('participantes_registo/',views.registo_view,name="participantes_registo"),
                  path('avaliadores_registo/',views.avaliadores_registo_view,name="avaliadores_registo"),
                  path('participant-overview/<int:participant_id>/', views.patient_overview_view,
                       name="participant-overview"),
                  path(
                      'gds-overview/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:patient_id>',
                      views.gds_overview_view,
                      name="gds-overview"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
