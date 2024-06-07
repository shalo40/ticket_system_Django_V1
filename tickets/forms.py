# tickets/forms.py

from django import forms
from .models import Ticket, Equipment, CustomUser, Comment, ServiceProcedure, ServiceType, WorkBudget, Diagnosis, DiagnosisTest

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'client', 'equipment', 'assigned_technician', 'service_type', 'description', 'is_remote']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['equipment'].queryset = Equipment.objects.filter(client=user)

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'components', 'operating_system']

class AssignTechnicianForm(forms.ModelForm):
    technician = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_technician=True), required=True)

    class Meta:
        model = Ticket
        fields = ['technician']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class TicketSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=False, label='Buscar')
    service_type = forms.ModelChoiceField(queryset=ServiceType.objects.all(), required=False, label='Tipo de Servicio')

class WorkBudgetForm(forms.ModelForm):
    class Meta:
        model = WorkBudget
        fields = ['service_procedure', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_procedure'].queryset = ServiceProcedure.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_cost = instance.service_procedure.cost * instance.quantity
        if commit:
            instance.save()
        return instance
    
class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['description']

class DiagnosisTestForm(forms.ModelForm):
    class Meta:
        model = DiagnosisTest
        fields = ['name', 'result', 'description']