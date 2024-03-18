from django.utils import timezone
from .models import *
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .game import *


def game_id_1min():
    game_time = timezone.now().second
    game_time_min = timezone.now().minute
    game_time_hour = timezone.now().hour
    time = 60 - game_time
    game_details_time = datetime.now()
    game_details = (
        GameDetail.objects.filter(game_name="1MIN").order_by("-created_at").first()
    )
    if game_details:
        dt_object = datetime.strptime(
            str(game_details.created_at), "%Y-%m-%d %H:%M:%S.%f%z"
        )
        timestamp = datetime.strptime(str(game_details_time), "%Y-%m-%d %H:%M:%S.%f")
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        formated_times = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        x = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
        y = datetime.strptime(formated_times, "%Y-%m-%d %H:%M:%S")
        time_diff = abs(x - y)
        if time == 5:
            # play_1min_game(game_details.game_type)
            print("game time is start", game_details.game_type)
            total_paid_amount, total_bet_amount, winning_amount = play_1min_game(
                game_details.game_type
            )
            print(total_paid_amount, total_bet_amount, winning_amount)
            print("game time is over")
        if time_diff >= timedelta(minutes=1):
            game_id = (
                "1MIN"
                + str(datetime.now().strftime("%Y%m%d"))
                + str(game_time_hour)
                + str(game_time_min)
                + str(game_time)
            )
            game_details = GameDetail.objects.create(
                game_type=game_id, game_name="1MIN", created_at=game_details_time
            )
        else:
            time = 60 - time_diff.seconds
    else:

        game_id = (
            "1MIN"
            + str(datetime.now().strftime("%Y%m%d"))
            + str(game_time_hour)
            + str(game_time_min)
            + str(game_time)
        )
        game_details = GameDetail.objects.create(
            game_type=game_id, game_name="1MIN", created_at=game_details_time
        )
    return game_details.game_type, time


def play_1min_game_status(game_id, time):
    # this function check game is still playing or not by chcking the game id , is_active status and by checking there is enough time left to play the game or not if there is only 5 sec left then it will play the game and return the game status is not active
    game_details = GameDetail.objects.filter(game_type=game_id, is_active=True).first()
    if not game_details:
        return False, "Game is not active"

    # check the game time is over or not
    # game_details = GameDetail.objects.filter(game_type=game_id).first()
    game_details_time = datetime.now()
    dt_object = datetime.strptime(
        str(game_details.created_at), "%Y-%m-%d %H:%M:%S.%f%z"
    )
    timestamp = datetime.strptime(str(game_details_time), "%Y-%m-%d %H:%M:%S.%f")
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    formated_times = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    x = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
    y = datetime.strptime(formated_times, "%Y-%m-%d %H:%M:%S")
    time_diff = abs(x - y)
    times = 180 - time_diff.seconds
    if time_diff >= timedelta(minutes=int(time)):
        return False, "Game is not active"
    elif times <= 5:
        return False, "Game is not active"
    else:
        return True, "Game is still active"


def game_id_3min():
    times = 180
    game_time_second = datetime.now().second
    game_time_min = datetime.now().minute
    game_time_hour = datetime.now().hour
    game_details_time = datetime.now()
    game_details = (
        GameDetail.objects.filter(game_name="3MIN").order_by("-created_at").first()
    )
    if game_details:
        dt_object = datetime.strptime(
            str(game_details.created_at), "%Y-%m-%d %H:%M:%S.%f%z"
        )
        timestamp = datetime.strptime(str(game_details_time), "%Y-%m-%d %H:%M:%S.%f")
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        formated_times = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        x = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
        y = datetime.strptime(formated_times, "%Y-%m-%d %H:%M:%S")
        time_diff = abs(x - y)
        if time_diff >= timedelta(minutes=3):
            game_id = (
                "3MIN"
                + str(datetime.now().strftime("%Y%m%d"))
                + str(game_time_hour)
                + str(game_time_min)
                + str(game_time_second)
            )
            game_details = GameDetail.objects.create(
                game_type=game_id, game_name="3MIN", created_at=game_details_time
            )
        else:
            times = 180 - time_diff.seconds

    else:
        game_id = (
            "3MIN"
            + str(datetime.now().strftime("%Y%m%d"))
            + str(game_time_hour)
            + str(game_time_min)
            + str(game_time_second)
        )
        game_details = GameDetail.objects.create(
            game_type=game_id, game_name="3MIN", created_at=game_details_time
        )
    return game_details.game_type, times


def check_game_times():
    """
    Function to check game times and send notifications to live users.

    This function retrieves the game type and time using the `game_id_1min` function,
    gets the channel layer, and sends a notification to each live user with the game time
    and game ID.

    Parameters:
        None

    Returns:
        None
    """
    print(" 1 min game scheduler started")
    game_type, time = game_id_1min()
    channel_layer = get_channel_layer()
    group_name = "game"
    liveUsers = liveUser.objects.filter(flag=1).all()
    for live_User in liveUsers:
        print(live_User)
        async_to_sync(channel_layer.send)(
            live_User.channel_name,
            {
                "type": "send_notification",
                "game_time": time,
                "game_id": game_type,
                "game_type": "1MIN",
            },
        )
        live_User.flag = 0
        live_User.save()
    print(time)
    if time == 60:
        liveUsers = liveUser.objects.all()
        for live_User in liveUsers:
            print(live_User, live_User.channel_name, game_type)
            async_to_sync(channel_layer.send)(
                live_User.channel_name,
                {
                    "type": "send_notification",
                    "game_time": time,
                    "game_id": game_type,
                    "game_type": "1MIN",
                },
            )
    print(" 1 min game scheduler ended")


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(check_game_times, "interval", seconds=1.8)
    scheduler.start()