import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from CityStars_app.models import Profile, User, Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)

    @sync_to_async
    def save(self, text, username, chat_id):
        profile = Profile.objects.get(user=User.objects.get(username=username))
        chat = Chat.objects.get(id=chat_id)
        message = Message(chat=chat, user=profile, text=text)
        message.save()
        return message

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        chat = text_data_json["chat"]
        messageObject = await self.save(message, username, chat)

        await self.channel_layer.group_send(
            self.roomGroupName,
            {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "sent": messageObject.sent_date.strftime("%H:%M"),
            },
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        sent = event["sent"]
        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "sent": sent}
            )
        )
