# tickets/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings



class CustomUser(AbstractUser):
    is_technician = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    pass

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_create_ticket", "Can create ticket"),
            ("can_assign_technician", "Can assign technician"),
            ("can_view_reports", "Can view reports"),
        ]
        
class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

User = get_user_model()
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Abierto'),
        ('IN_PROGRESS', 'En Progreso'),
        ('CLOSED', 'Cerrado'),
    ]
    title = models.CharField(max_length=100, default='Título por defecto')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='tickets')
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_remote = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_type.name} - {self.status}"

class Equipment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='equipments')
    name = models.CharField(max_length=100)
    components = models.TextField()
    operating_system = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.id} - {self.action} - {self.timestamp}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username} - {self.message}"

class ServiceProcedure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class WorkBudget(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='work_budgets')
    service_procedure = models.ForeignKey(ServiceProcedure, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Presupuesto para Ticket #{self.ticket.id} - {self.service_procedure.name}"

class Diagnosis(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='diagnoses')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Diagnosis for Ticket #{self.ticket.id}'

class DiagnosisTest(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(max_length=100)
    description = models.TextField()
    result = models.CharField(max_length=100)

    def __str__(self):
        return self.name