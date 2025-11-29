"""
Management command to create the 'Sacrament Editors' group.
Run this after migrations: python manage.py create_sacrament_editors_group
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates Sacrament Editors group'

    def handle(self, *args, **options):
        # Create or get the group
        group, created = Group.objects.get_or_create(name='Sacrament Editors')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Sacrament Editors" group'))
            self.stdout.write(self.style.SUCCESS(
                'Add users to this group in Django admin to allow them to manage sacrament records'
            ))
        else:
            self.stdout.write(self.style.WARNING('"Sacrament Editors" group already exists'))
