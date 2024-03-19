from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
import json
from .models import *
from datetime import datetime
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import parse_qs
from .game import *
from .scheduler import *


class GameClockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = "game"
        await self.channel_layer.group_add(group_name, self.channel_name)
        query_string = self.scope["query_string"]
        query_params = parse_qs(query_string.decode("utf-8"))
        user_id = query_params.get("user_id", [None])[0]
        self.user_id = user_id
        await self.accept()
        if not user_id:
            await self.send(
                {
                    "type": "websocket.close",
                    "code": 4000,
                    "reason": "user_id is required",
                }
            )
            await self.close()
        await sync_to_async(liveUser.objects.update_or_create)(
            user_id_id=user_id,
            defaults={"channel_name": self.channel_name, "flag": 1},
        )

    async def disconnect(self, close_code):
        await sync_to_async(liveUser.objects.filter(channel_name=self.channel_name).delete)()
        await self.close()

    async def send_game_time(self, game_time, game_id, type):
        await self.send(
            text_data=json.dumps(
                {"game_time": game_time, "game_id": game_id, "game_type": type}
            )
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def receive(self, text_data):
        data = json.loads(text_data)
        game_id = data["game_id"]
        user_id = data["user_id"]
        amount = data["amount"]
        game_type = data["type_of_bet"]
        bet = data["bet"]
        if data["game_type"] == "1 minute":
            # check time to play the game if 5 seconds is left then user can't play the game
            health, time = await sync_to_async(play_1min_game_status)(game_id, 1)
            print(health, time)
            print("8" * 100)
            if not health:
                await self.send(text_data=json.dumps({"error": time}))
                return
            # check user balance
            user = await sync_to_async(UserDetail.objects.get)(id=user_id)
            if user.wallet < amount:
                await self.send(text_data=json.dumps({"error": "Insufficient balance"}))
                return
            # deduct amount from user wallet
            user.wallet -= amount
            await sync_to_async(user.save)()
            # play game
            game_id_id = await sync_to_async(GameDetail.objects.filter(game_type=game_id).first)().id
            game_datas = await sync_to_async(UserGameData.objects.create)(
                game_type=game_type,
                game_id_id=game_id_id,
                amount=amount,
                user_id_id=user_id,
                type_of_bet=game_type,
                bet=bet,
            )
            await self.send(
                text_data=json.dumps(
                    {"message": "Game played successfully", "bet_id": game_datas.id}
                )
            )


# UserGameData(
#     game_type="1 minute",
#     game_id_id= GameDetail.objects.filter(game_type="1MIN20240316165655").first().id,
#     type_of_bet="big/small",
#     bet="big",
#     amount=100,
#     user_id_id = UserDetail.objects.get(id=1).id

# ).save()
# UserGameData(
#     game_type="1 minute",
#     game_id_id= GameDetail.objects.filter(game_type="1MIN20240316165655").first().id,
#     type_of_bet="number",
#     bet="1",
#     amount=100,
#     user_id_id =  UserDetail.objects.get(id=1).id

# ).save()

import random
import random


def calculate_winning_number(bet):
    color_and_number_of_balls = {
        "0": ["red", "violet", "small"],
        "1": ["green", "small"],
        "2": ["red", "small"],
        "3": ["green", "small"],
        "4": ["red", "small"],
        "5": ["green", "violet", "big"],
        "6": ["red", "big"],
        "7": ["green", "big"],
        "8": ["red", "big"],
        "9": ["green", "big"],
    }

    total_amount = sum([b["amount"] for b in bet])
    winning_amount = total_amount * 0.9  # 90% of total betting amount

    while True:
        winning_number = str(random.randint(0, 9))
        ball = color_and_number_of_balls[winning_number]
        amount = 0
        for b in bet:
            if b["type_of_bet"] == "big/small" and b["bet"] == ball[-1]:
                amount += b["amount"] * 2
            elif b["type_of_bet"] == "color" and b["bet"] in ball[0:-1]:
                amount += b["amount"] * 2 if b["bet"] != "violet" else b["amount"] * 4.5
            elif b["type_of_bet"] == "number" and str(b["bet"]) == str(winning_number):
                amount += b["amount"] * 8
        if amount <= winning_amount:
            break
    return winning_number, amount, total_amount, ball[0:-1], ball[-1]


@receiver(post_save, sender=GameDetail)
def game_detail_post_save(sender, instance, created, **kwargs):
    if created:
        print(instance, "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        channel_layer = get_channel_layer()
        liveUsers = liveUser.objects.all()
        for live_User in liveUsers:
            print(live_User, live_User.channel_name, instance.game_type)
            async_to_sync(channel_layer.send)(
                live_User.channel_name,
                {
                    "type": "send_notification",
                    "game_time": 60,
                    "game_id": instance.game_type,
                    "game_type": "1MIN",
                },
            )
