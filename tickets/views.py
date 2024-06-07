# tickets/views.py
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Ticket, Equipment, ServiceType, CustomUser, TicketHistory, Comment, WorkBudget, ServiceProcedure, Diagnosis, DiagnosisTest
from .forms import TicketForm, EquipmentForm, AssignTechnicianForm, CommentForm, TicketSearchForm, WorkBudgetForm, DiagnosisForm, DiagnosisTestForm
from django.db.models import Count

@login_required
def dashboard(request):
    if request.method == 'GET':
        form = TicketSearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data.get('search_term')
            service_type = form.cleaned_data.get('service_type')
            tickets = Ticket.objects.all()
            if search_term:
                tickets = tickets.filter(description__icontains=search_term)
            if service_type:
                tickets = tickets.filter(service_type=service_type)
        else:
            tickets = Ticket.objects.all()
    else:
        form = TicketSearchForm()
        tickets = Ticket.objects.all()
    
    if request.user.is_client:
        tickets = tickets.filter(client=request.user)
    elif request.user.is_technician:
        tickets = tickets.filter(technician=request.user)
    
    return render(request, 'tickets/dashboard.html', {'tickets': tickets, 'form': form})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.client = request.user
            ticket.save()
            # Registrar acción
            TicketHistory.objects.create(ticket=ticket, action='Ticket creado')
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def add_equipment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.ticket = ticket
            equipment.save()
            # Registrar acción
            TicketHistory.objects.create(ticket=ticket, action='Equipo agregado')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = EquipmentForm()
    return render(request, 'tickets/add_equipment.html', {'form': form, 'ticket': ticket})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    diagnoses = Diagnosis.objects.filter(ticket=ticket)
    work_budgets = WorkBudget.objects.filter(ticket=ticket)
    comments = Comment.objects.filter(ticket=ticket)
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'diagnoses': diagnoses,
        'work_budgets': work_budgets,
        'comments': comments,
    })

@login_required
def assign_technician(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = AssignTechnicianForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            # Registrar acción
            TicketHistory.objects.create(ticket=ticket, action='Técnico asignado')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = AssignTechnicianForm(instance=ticket)
    return render(request, 'tickets/assign_technician.html', {'form': form, 'ticket': ticket})

@login_required
def report(request):
    tickets_by_status = Ticket.objects.values('status').annotate(count=Count('status'))
    tickets_by_service = Ticket.objects.values('service_type__name').annotate(count=Count('service_type'))
    return render(request, 'tickets/report.html', {
        'tickets_by_status': tickets_by_status,
        'tickets_by_service': tickets_by_service,
    })

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all()
    return render(request, 'tickets/notifications.html', {'notifications': user_notifications})

@login_required
@permission_required('tickets.can_view_reports', raise_exception=True)
def export_tickets_csv(request):
    # Crear la respuesta con tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

    # Crear un escritor CSV
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Tipo de Servicio', 'Estado', 'Cliente', 'Fecha de Creación'])

    # Obtener los tickets
    tickets = Ticket.objects.all()
    for ticket in tickets:
        writer.writerow([
            ticket.id, 
            ticket.service_type.name, 
            ticket.get_status_display(), 
            ticket.client.username, 
            ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response

@login_required
@permission_required('tickets.can_create_ticket', raise_exception=True)
def add_work_budget(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = WorkBudgetForm(request.POST)
        if form.is_valid():
            work_budget = form.save(commit=False)
            work_budget.ticket = ticket
            work_budget.save()
            messages.success(request, 'El presupuesto de trabajo se ha añadido correctamente.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = WorkBudgetForm()
    return render(request, 'tickets/add_work_budget.html', {'form': form, 'ticket': ticket})

@login_required
@permission_required('tickets.can_create_ticket', raise_exception=True)
def add_diagnosis(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.ticket = ticket
            diagnosis.save()
            messages.success(request, 'El diagnóstico se ha añadido correctamente.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = DiagnosisForm()
    return render(request, 'tickets/add_diagnosis.html', {'form': form, 'ticket': ticket})

@login_required
def add_diagnosis_test(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    if request.method == 'POST':
        form = DiagnosisTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.diagnosis = diagnosis
            test.save()
            return redirect('ticket_detail', ticket_id=diagnosis.ticket.id)
    else:
        form = DiagnosisTestForm()
    return render(request, 'tickets/add_diagnosis_test.html', {'form': form, 'diagnosis': diagnosis})

@login_required
def add_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user  # Asignar el usuario actual como autor
            comment.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = CommentForm()

    return render(request, 'tickets/add_comment.html', {'form': form, 'ticket': ticket})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comments = ticket.comments.all()
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'comments': comments})