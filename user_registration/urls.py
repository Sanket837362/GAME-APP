from django.urls import path
from .views import *
urlpatterns = [

    #############################  USER REGISTRATION  ################################
    path('register/', UserRegistration.as_view(), name='register'),
    path('get/', UserRegistration.as_view(), name='get'),
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
    path('user-current-game-result/', UserGameDataAPI.as_view(), { "slug": "user-current-game-result" },name='user-current-game-result'),

    #############################  BANK DETAILS  ################################
    path('add-bank-details/', UserBankAPI.as_view(), name='bank_details'),
    path('update-bank-details/', UserBankAPI.as_view(), name='update_bank_details'),
    path('get-bank-details/', UserBankAPI.as_view(), name='get_bank_details'),
    path('withdraw-money/',  UserwithdrawHistoryAPi.as_view(), name='withdraw_money'),
    path('withdraw-money-history/',  UserwithdrawHistoryAPi.as_view(), name='withdraw_money_history'),

    path('deposit-money/',  UserDepositHistoryAPi.as_view(), name='Depositmoney'),
    path('deposit-money-history/',  UserDepositHistoryAPi.as_view(), name='Deposit_money_history'),

]