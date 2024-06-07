

# tickets/admin.py

from django.contrib import admin
from .models import Ticket, Equipment, Comment, Diagnosis, DiagnosisTest, WorkBudget, ServiceType, TicketHistory, Notification, ServiceProcedure, CustomUser
from django.contrib.auth.admin import UserAdmin


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'service_type', 'status', 'client', 'created_at']
    search_fields = ['title', 'client__username', 'service_type__name']
    list_filter = ['status', 'service_type']

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ticket']
    search_fields = ['name', 'ticket__title']
    list_filter = ['ticket']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'author', 'text', 'date_created']
    search_fields = ['ticket__title', 'author__username']
    list_filter = ['date_created']

class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'description', 'date_created']
    search_fields = ['ticket__title']
    list_filter = ['date_created']

class DiagnosisTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'diagnosis', 'name', 'result']
    search_fields = ['diagnosis__description', 'name']
    list_filter = ['result']

class WorkBudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'service_procedure', 'quantity', 'total_cost', 'created_at']
    search_fields = ['ticket__title', 'service_procedure__name']
    list_filter = ['created_at']

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'action', 'timestamp']
    search_fields = ['ticket__title', 'action']
    list_filter = ['timestamp']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'read', 'created_at']
    search_fields = ['user__username', 'message']
    list_filter = ['read', 'created_at']

class ServiceProcedureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'cost']
    search_fields = ['name', 'description']
    list_filter = ['cost']

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_technician', 'is_client', 'is_admin']
    search_fields = ['username', 'email']
    list_filter = ['is_technician', 'is_client', 'is_admin']

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(DiagnosisTest, DiagnosisTestAdmin)
admin.site.register(WorkBudget, WorkBudgetAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(TicketHistory, TicketHistoryAdmin)
admin.site.register(Notification, NotificationAdmin)








admin.site.register(CustomUser, UserAdmin)
admin.site.register(ServiceProcedure)