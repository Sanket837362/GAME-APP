from django.urls import path
from .views import *
urlpatterns = [

    #############################  USER REGISTRATION  ################################
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),

    #############################  GAME CLOCK  ################################
    path('game_clock/', GameClock.as_view(), name='game_clock'),

    #############################  USER PAYMENT DEPOSIT  ################################
    path('user_payment/', UserPayment.as_view(), name='user_payment'),
    path('user_payment_history/', UserPayment.as_view(), name='user_payment_history'),

    #############################  GAME HISTORY  ################################
    path('game-history/', GameHistory.as_view(), name='game_history'),

    #############################  USER GAME DATA  ################################
    path('place-bet/', UserGameDataAPI.as_view(), name='place_bet'),
    path('user-game-result/', UserGameDataAPI.as_view(), name='user-game-result'),

    #############################  BANK DETAILS  ################################
    path('add-bank-details/', UserBankAPI.as_view(), name='bank_details'),
    path('update-bank-details/', UserBankAPI.as_view(), name='update_bank_details'),
    path('get-bank-details/', UserBankAPI.as_view(), name='get_bank_details'),


]