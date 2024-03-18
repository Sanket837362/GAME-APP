

from .models import *
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from django.contrib.auth.hashers import make_password , check_password
from datetime import datetime, timedelta
from random_username.generate import generate_username

class UserRegistration(ListAPIView):
    def post(self,request):
        try:
            data = request.data
            data['username'] = generate_username(1)[0]
            while UserDetail.objects.filter(username=data['username']).exists():
                data['username'] = generate_username(1)[0]
            password = make_password(data['password'])
            if data['password'] != data['confirm_password']:
                return Response({"message":"Password and confirm password not match"})
            if data.get('email') and UserDetail.objects.filter(email= data.get('email')).exists():
                return Response({"message":"email already exists"})
            if data.get('phone') and UserDetail.objects.filter(phone=data.get('phone')).exists():
                return Response({"message":"phone already exists"})
            data['password'] = password
            data.pop('confirm_password')
            user = UserDetail.objects.create(**data)
            return Response({"message":"User created successfully","data":user.id})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request):
        try:
            id = request.GET.get('id')
            if id:
                user = UserDetail.objects.filter(id=id).values()
                return Response({"data":user})
            user = UserDetail.objects.all().values()
            return Response({"data":user})
        except Exception as e:
            return Response({"message":str(e)})
        



class Login(ListAPIView):
    def post(self,request):
        try:
            data = request.data
            if not data.get('phone') and not data.get('email'):
                return Response({"message":"Phone or email is required"})
            phone=data.get('phone')
            email=data.get('email')
            user = UserDetail.objects.filter(phone=phone).values().first() if phone else UserDetail.objects.filter(email=email).values().first()
            if user:
                if check_password(data['password'],user['password']):
                    return Response({"message":"Login successfully","data":user })
                return Response({"message":"Invalid password"})
            return Response({"message":"Invalid phone"})
        except Exception as e:
            return Response({"message":str(e)})

class UserPayment(ListAPIView):
    def post(self,request):
        try:
            data = request.data
            user = UserDetail.objects.filter(id=data['user_id']).first()
            if user:
                if data['status'] == "done":
                    user.wallet += data['amount']
                UserPaymentModel.objects.create(
                    user_id = user,
                    amount = data['amount'],
                    upi_id = data['upi_id'],
                    status = data['status']
                )
                user.save()
                return Response({"message":"Payment added successfully"})
            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request):
        try:
            id = request.GET.get('id')
            if id:
                print(id)
                user = UserPaymentModel.objects.filter(user_id=id).values()
                print(user)
                return Response(user)
            return Response({"data": "id is required"})
        except Exception as e:
            return Response({"message":str(e)})

class GameHistory(ListAPIView):
    def get(self,request):
        try:
            game = result.objects.all().extra(
            select={
                "winning_color_cleaned": '''replace(replace(replace(winning_color, '[', ''), ']', ''), "'", "")'''
                        }
                    ).values(
                        "game_id__game_type",
                        "winning_number",
                        "winning_color_cleaned",
                        "winning_ball"
                    )
            return Response({"data":game})
        except Exception as e:
            return Response({"message":str(e)})
        
class UserGameDataAPI(ListAPIView):
    def post(self,request):
        try:
            data = request.data
            user = UserDetail.objects.filter(id=data['user_id']).first()
            if user:
                if user.wallet < data['amount']:
                    return Response({"message":"Insufficient balance"})
                user.wallet -= data['amount']
                user.save()
                game_id_id = GameDetail.objects.filter(game_type=data['game_id']).first().id
                UserGameData.objects.create(
                    game_type = data['game_type'],
                    game_id_id = game_id_id,
                    amount = data['amount'],
                    user_id = user,
                    type_of_bet = data['type_of_bet'],
                    bet = data['bet']
                )
                return Response({"message":"Game played successfully"})
            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request):
        try:
            id = request.GET.get('user_id')
            if id:
                game = UserGameData.objects.filter(user_id_id=id).extra(
            select={
                "winning_color_cleaned": '''replace(replace(replace(winning_color, '[', ''), ']', ''), "'", "")'''
                        }
                    ).values( "game_type", "amount", "type_of_bet", "bet" , "win_or_lose" , "winning_amount" , "winning_number", "winning_ball" , "created_at" , "game_id__game_type" ,'winning_color_cleaned')
                return Response({"data":game})
            game = UserGameData.objects.all().values()
            return Response({"data":game})
        except Exception as e:
            return Response({"message":str(e)})

