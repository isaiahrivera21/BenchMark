import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a group to broadcast messages
        await self.channel_layer.group_add("metrics_updates", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("metrics_updates", self.channel_name)


    async def receive(self, text_data):
        pass  # Not needed for simple broadcasting 

    async def metrics_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"data": message}))   

class AllTimeMacrosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("all_time_macros_updates", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("all_time_macros_updates", self.channel_name)

    async def receive(self, text_data):
        pass

    async def all_time_macros_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"data": message}))

class WeeklyMacrosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("weekly_macros_updates", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("weekly_macros_updates", self.channel_name)

    async def receive(self, text_data):
        pass

    async def weekly_macros_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"data": message}))


class MonthlyMacrosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("monthly_macros_updates", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("monthly_macros_updates", self.channel_name)

    async def receive(self, text_data):
        pass

    async def monthly_macros_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"data": message}))
