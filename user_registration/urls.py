from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('user_payment/', UserPayment.as_view(), name='user_payment'),
    path('user_payment_history/', UserPayment.as_view(), name='user_payment_history'),
    path('game-history/', GameHistory.as_view(), name='game_history'),
    path('place-bet/', UserGameDataAPI.as_view(), name='place_bet'),
    path('user-game-result/', UserGameDataAPI.as_view(), name='user-game-result'),

]