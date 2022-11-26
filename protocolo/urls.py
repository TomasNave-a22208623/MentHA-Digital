from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# app_name = "protocolo"

urlpatterns = [
                  path('', views.protocolos_view, name="protocols"),
                  path('dashboard', views.dashboard_view, name="dashboard"),
                  path('protocol-participants/<int:protocol_id>', views.protocol_participants_view,
                       name="protocol-participants"),
                  path('participants', views.participants_view, name="participants"),
                  path('dashboard-content', views.dashboard_content_view, name="dashboard-content"),
                  path('parts/<int:protocol_id>/<int:patient_id>', views.parts_view, name="parts"),
                  path('areas/<int:protocol_id>/<int:part_id>/<int:patient_id>', views.areas_view, name="areas"),
                  path('instruments/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:patient_id>',
                       views.instruments_view,
                       name="instruments"),
                  path('dimension/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:patient_id>',
                       views.dimensions_view, name="dimensions"),
                  path(
                      'section/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:dimension_id>/<int:patient_id>',
                      views.sections_view, name="sections"),
                  path(
                      'question/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:dimension_id>/<int:section_id>/<int:patient_id>',
                      views.question_view, name="question"),
                  path('report/<int:resolution_id>', views.report_view, name="report"),
                  path('login', views.login_view, name="login"),
                  path('logout', views.logout_view, name="logout"),
                  path('profile/<int:participant_id>/', views.profile_view, name="participant"),
                  path('participant-overview/<int:participant_id>/', views.patient_overview_view,
                       name="participant-overview"),
                  path('gds-overview/<int:protocol_id>/<int:part_id>/<int:area_id>/<int:instrument_id>/<int:patient_id>', views.gds_overview_view,
                       name="gds-overview"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
