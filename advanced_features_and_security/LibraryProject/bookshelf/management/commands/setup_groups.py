# LibraryProject/bookshelf/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Set up initial groups and permissions"

    def handle(self, *args, **kwargs):
        # Fetch permissions
        perms = {
            "can_view": Permission.objects.get(codename="can_view"),
            "can_create": Permission.objects.get(codename="can_create"),
            "can_edit": Permission.objects.get(codename="can_edit"),
            "can_delete": Permission.objects.get(codename="can_delete"),
        }

        # Create groups
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        # Assign permissions
        viewers.permissions.set([perms["can_view"]])
        editors.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"]])
        admins.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"], perms["can_delete"]])

        self.stdout.write(self.style.SUCCESS("Groups and permissions created successfully."))
