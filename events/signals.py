from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from .services import WhatsAppService

@receiver(post_save, sender=Event)
def send_whatsapp_notification(sender, instance, created, **kwargs):
    if created:
        message = f"*{instance.title}*\n\n{instance.description}"
        WhatsAppService.send_broadcast(message)
