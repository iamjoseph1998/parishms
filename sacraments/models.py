from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class SacramentType(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Baptism, Marriage")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MemberSacrament(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sacraments')
    sacrament_type = models.ForeignKey(SacramentType, on_delete=models.CASCADE)
    sacrament_date = models.DateField()
    notes = models.TextField(blank=True)
    
    # Full audit trail - tracks every change
    history = HistoricalRecords()

    class Meta:
        unique_together = ('member', 'sacrament_type')

    def __str__(self):
        return f"{self.member} - {self.sacrament_type}"
