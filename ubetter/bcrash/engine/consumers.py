# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import GameProfit  # Replace with your actual model

class DatabaseChangeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    @receiver(post_save, sender=GameProfit)
    async def handle_database_change(sender, instance, **kwargs):
        await sender.send(text_data=json.dumps({'message': 'Database change detected'}))
