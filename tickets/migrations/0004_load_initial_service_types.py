# tickets/migrations/0002_load_initial_service_types.py

from django.db import migrations

def load_initial_service_types(apps, schema_editor):
    ServiceType = apps.get_model('tickets', 'ServiceType')
    service_types = [
        {'name': 'Reparación de Computadoras', 'description': 'Servicio de reparación y mantenimiento de computadoras.'},
        {'name': 'Consultoría IT', 'description': 'Consultoría en tecnología de la información.'},
        {'name': 'Desarrollo de Software', 'description': 'Servicios de desarrollo de aplicaciones y software a medida.'},
        {'name': 'Instalación de Redes', 'description': 'Instalación y configuración de redes informáticas.'},
        {'name': 'Mantenimiento de Servidores', 'description': 'Mantenimiento preventivo y correctivo de servidores.'},
    ]
    
    for service_type in service_types:
        ServiceType.objects.create(**service_type)

class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),  # Asegúrate de que esto apunte a la última migración de tu modelo.
    ]

    operations = [
        migrations.RunPython(load_initial_service_types),
    ]