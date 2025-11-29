from django.db import models
from django.conf import settings
from accounts.models import UserRole

class Family(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., 'The Smith Family'")
    family_head = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='headed_family',
        limit_choices_to={'role': UserRole.FAMILY_HEAD}
    )
    # members accessed via related_name='family' from AccountUser

    def __str__(self):
        return self.name

    def handle_head_death(self, new_head_user):
        """
        Deactivates old head, promotes new user to head, and updates relationship.
        """
        old_head = self.family_head
        
        # Deactivate old head
        old_head.is_active = False
        old_head.save()

        # Promote new head
        new_head_user.role = UserRole.FAMILY_HEAD
        new_head_user.family = None # Head is linked via OneToOne, not ForeignKey
        new_head_user.save()

        # Update Family
        self.family_head = new_head_user
        self.save()
