import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import MealEvent, Message

User = get_user_model()

class EventConsumer(WebsocketConsumer):
    def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f'event_{self.event_id}'
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        
        # Save message to database
        user = User.objects.get(id=user_id)
        event = MealEvent.objects.get(id=self.event_id)
        Message.objects.create(
            event=event,
            user=user,
            content=message
        )
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'username': user.username
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        username = event['username']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'username': username
        })) 