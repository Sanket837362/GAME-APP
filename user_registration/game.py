import random
from .models import *
from django.db.models import Sum, F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

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

    total_amount = sum([b["total_amount"] for b in bet])
    winning_amount = total_amount * 0.98  # 90% of total betting amount

    while True:
        winning_number = str(random.randint(0, 9))
        ball = color_and_number_of_balls[winning_number]
        amount = 0
        for b in bet:
            if b["type_of_bet"] == "big/small" and b["bet"] == ball[-1]:
                amount += b["total_amount"] * 2
            elif b["type_of_bet"] == "color" and b["bet"] in ball[0:-1]:
                amount += (
                    b["total_amount"] * 2
                    if b["bet"] != "violet"
                    else b["total_amount"] * 4.5
                )
            elif b["type_of_bet"] == "number" and str(b["bet"]) == str(winning_number):
                amount += b["total_amount"] * 8
        if amount <= winning_amount:
            break
    return winning_number, winning_amount, amount, ball[0:-1], ball[-1]


def play_1min_game(game_id):
    games_data = GameDetail.objects.filter(game_type=game_id, is_active=True)
    if not games_data:
        return "Game not found", None, None

    bets = (
        UserGameData.objects.filter(game_id__game_type=game_id, game_id__is_active=True)
        .values("type_of_bet", "bet")
        .annotate(total_amount=Sum("amount"))
    )
    winning_number, total_bet_amount, winning_amount, color, big_small = (
        calculate_winning_number(list(bets))
    )
    game_id_id = GameDetail.objects.filter(game_type=game_id).first().id
    result.objects.create(
        game_id_id=game_id_id,
        winning_number=winning_number,
        winning_color=color,
        winning_ball=big_small,
        total_bet_amount=total_bet_amount,
        total_win_amount=winning_amount,
    )
    user_data = UserGameData.objects.filter(game_id__game_type=game_id)
    total_paid_amount = 0
    for user in user_data:
        amount = 0
        bet_amount = user.amount * 0.98
        if user.type_of_bet == "big/small" and user.bet == big_small:
            amount += bet_amount * 2
        elif user.type_of_bet == "color" and user.bet in color:
            if user.bet == "violet":
                amount += bet_amount * 4.5
            else:
                if user.bet == "red" and winning_number == "0":
                    amount += bet_amount * 1.5
                # else:
                #     amount += bet_amount * 2
                elif user.bet == "green" and winning_number == "5":
                    amount += bet_amount * 1.5
                else:
                    amount += bet_amount * 2

        elif user.type_of_bet == "number" and str(user.bet) == str(winning_number):
            amount += bet_amount * 8
        if amount > 0:
            user.win_or_lose = "win"
            user.winning_amount = amount
            user.winning_number = winning_number
            user.winning_color = color
            user.winning_ball = big_small
            user.save()
            UserDetail.objects.filter(id=user.user_id.id).update(
                wallet=F("wallet") + amount
            )
            total_paid_amount += amount

        else:
            user.win_or_lose = "lose"
            user.winning_amount = 0
            user.winning_number = winning_number
            user.winning_color = color
            user.winning_ball = big_small
            user.save()
        live_User = liveUser.objects.filter(user_id_id =  user.user_id.id).first()
        print(live_User,"REsulfghjdsbjdbfhsdjkfjyhadhfuiycern8iuynw348iry8urwiytureyvtuiyuiytuwrvtuiyrvytuerytuvreyuivtuiyruitvyuithoiyyujhweg vyugj")
        if live_User:
            channel_layer = get_channel_layer()
            print(live_User, live_User.channel_name)
            async_to_sync(channel_layer.send)(
                live_User.channel_name,
                {
                    "type": "send_notification",
                    "message": f"You have {user.win_or_lose} on 1MIN Game." ,
                    "notification_type": "Result",
                },
            )

    games_data.update(is_active=False)
    return total_paid_amount, total_bet_amount, winning_amount
