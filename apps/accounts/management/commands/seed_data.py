from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.patients.models import Patient
from apps.tests.models import TestType, TestRequest


class Command(BaseCommand):
    help = 'Seeds demo data for SmartLab Manager'

    def handle(self, *args, **options):
        User = get_user_model()
        users = [
            ('admin', 'admin', 'Admin', 'admin@example.com'),
            ('labtech', 'lab_tech', 'Lab Tech', 'labtech@example.com'),
            ('reception', 'receptionist', 'Reception', 'reception@example.com'),
        ]
        created_users = {}
        for username, role, full_name, email in users:
            user, created = User.objects.get_or_create(username=username, defaults={'role': role, 'email': email, 'first_name': full_name})
            user.role = role
            user.set_password('admin12345')
            user.email = email
            user.save()
            created_users[role] = user

        test_types = [
            ('Malaria Test', 'Rapid malaria diagnosis', 'Negative / Positive', 500),
            ('CBC', 'Complete blood count', '4.5 - 11.0', 1200),
            ('Blood Sugar', 'Glucose level check', '70 - 140 mg/dL', 300),
        ]
        type_objs = []
        for name, description, normal_range, price in test_types:
            obj, _ = TestType.objects.get_or_create(name=name, defaults={'description': description, 'normal_range': normal_range, 'price': price})
            type_objs.append(obj)

        if not Patient.objects.exists():
            patient1 = Patient.objects.create(full_name='Amina Otieno', patient_number='PT-001', gender='Female', date_of_birth='2001-04-12', phone='0700000001', address='Kisumu')
            patient2 = Patient.objects.create(full_name='Brian Ouma', patient_number='PT-002', gender='Male', date_of_birth='1999-09-23', phone='0700000002', address='Maseno')
            TestRequest.objects.get_or_create(patient=patient1, test_type=type_objs[0], requested_by=created_users['receptionist'], assigned_to=created_users['lab_tech'])
            TestRequest.objects.get_or_create(patient=patient2, test_type=type_objs[1], requested_by=created_users['admin'], assigned_to=created_users['lab_tech'])

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
