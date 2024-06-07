from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', lambda request: redirect('accounts/login')),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('add_equipment/<int:ticket_id>/', views.add_equipment, name='add_equipment'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('assign_technician/<int:ticket_id>/', views.assign_technician, name='assign_technician'),
    path('report/', views.report, name='report'),
    path('notifications/', views.notifications, name='notifications'),
    path('export_tickets_csv/', views.export_tickets_csv, name='export_tickets_csv'),
    path('add_work_budget/<int:ticket_id>/', views.add_work_budget, name='add_work_budget'),
    path('add_diagnosis/<int:ticket_id>/', views.add_diagnosis, name='add_diagnosis'),
    path('add_diagnosis_test/<int:diagnosis_id>/', views.add_diagnosis_test, name='add_diagnosis_test'),
    path('ticket/<int:ticket_id>/add_comment/', views.add_comment, name='add_comment'),
    
]
