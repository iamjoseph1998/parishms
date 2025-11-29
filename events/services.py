import requests
from django.conf import settings
from accounts.models import AccountUser

class WhatsAppService:
    @staticmethod
    def send_message(phone_number, message):
        """
        Sends a WhatsApp message to a single number.
        """
        if not settings.WHATSAPP_API_KEY:
            print(f"[Mock WhatsApp] Sending to {phone_number}: {message}")
            return

        headers = {
            'Authorization': f'Bearer {settings.WHATSAPP_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'text',
            'text': {'body': message},
        }
        try:
            response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=data)
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

    @staticmethod
    def send_broadcast(message):
        """
        Sends a message to all users with a valid phone number.
        """
        users = AccountUser.objects.exclude(phone_number__isnull=True).exclude(phone_number='')
        print(f"Broadcasting to {users.count()} users...")
        for user in users:
            WhatsAppService.send_message(user.phone_number, message)
