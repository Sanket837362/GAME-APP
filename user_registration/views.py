

from .scheduler import game_id_1min , game_id_3min, game_id_5min, game_id_10min
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
                return Response(user[0])
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
                return Response({"message":"Payment failed"})

            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request):
        try:
            id = request.GET.get('id')
            if id:
                user = UserPaymentModel.objects.filter(user_id=id).values()
                return Response(user)
            return Response({"data": "id is required"})
        except Exception as e:
            return Response({"message":str(e)})

class GameHistory(ListAPIView):
    def get(self,request):
        try:
            game_type = request.GET.get('game_type')
            if not game_type or game_type not in ["1MIN","3MIN","5MIN","10MIN"]:
                return Response({"message":"game_type is required and should be 1MIN or 3MIN or 5MIN or 10MIN"})
            game = result.objects.filter(game_type=game_type).extra(
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
            '''
            payload = {
                "user_id":1,
                "game_id":1,
                "type_of_bet":"big/small",
                "bet":"big",
                "amount":100
                "game_type":"1MIN" or "3MIN" or "5MIN" or "10MIN"
            }
            '''
            data = request.data
            user = UserDetail.objects.filter(id=data['user_id']).first()
            if user:
                if user.wallet < data['amount']:
                    return Response({"message":"Insufficient balance"})
                
                game_id_id = GameDetail.objects.filter(game_type=data['game_id'] , is_active=True ,  game_name = data['game_type']).first()

                if game_id_id:
                    if data['game_type'] == "1MIN":
                        game_type, time = game_id_1min()
                        if time < 5:
                            return Response({"message":"Game is Almost finished"})
                        else:
                            bet_id=UserGameData.objects.create(
                                user_id = user,
                                game_id = game_id_id,
                                type_of_bet = data['type_of_bet'],
                                bet = data['bet'],
                                amount = data['amount']*0.98,
                                game_type = game_type
                            )
                            user.wallet -= data['amount']
                            user.save()
                            return Response({"message":"Bet placed successfully" ,"bet_id":bet_id.id , "wallet":user.wallet})
                    elif data['game_type'] == "3MIN":
                        game_type, time = game_id_3min()
                        if time < 5:
                            return Response({"message":"Game is Almost finished"})
                        else:
                            bet_id=UserGameData.objects.create(
                                user_id = user,
                                game_id = game_id_id,
                                type_of_bet = data['type_of_bet'],
                                bet = data['bet'],
                                amount = data['amount']*0.98,
                                game_type = game_type
                            )
                            user.wallet -= data['amount']
                            user.save()
                            return Response({"message":"Bet placed successfully" ,"bet_id":bet_id.id , "wallet":user.wallet})
                    elif data['game_type'] == "5MIN":
                        game_type, time = game_id_5min()
                        if time < 5:
                            return Response({"message":"Game is Almost finished"})
                        else:
                            bet_id=UserGameData.objects.create(
                                user_id = user,
                                game_id = game_id_id,
                                type_of_bet = data['type_of_bet'],
                                bet = data['bet'],
                                amount = data['amount']*0.98,
                                game_type = game_type
                            )
                            user.wallet -= data['amount']
                            user.save()
                            return Response({"message":"Bet placed successfully" ,"bet_id":bet_id.id , "wallet":user.wallet})
                    elif data['game_type'] == "10MIN":
                        game_type, time = game_id_10min()
                        if time < 5:
                            return Response({"message":"Game is Almost finished"})
                        else:
                            bet_id=UserGameData.objects.create(
                                user_id = user,
                                game_id = game_id_id,
                                type_of_bet = data['type_of_bet'],
                                bet = data['bet'],
                                amount = data['amount']*0.98,
                                game_type = game_type
                            )
                            user.wallet -= data['amount']
                            user.save()
                            return Response({"message":"Bet placed successfully" ,"bet_id":bet_id.id , "wallet":user.wallet})
                    else:
                        return Response({"message":"Game type not found"})
                return Response({"message":"Game not found"})
            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request, slug = None):
        try:
            if not slug:
                id = request.GET.get('user_id')
                game_type = request.GET.get('game_type')
                if not game_type or game_type not in ["1MIN","3MIN","5MIN","10MIN"]:
                    return Response({"message":"game_type is required and should be 1MIN or 3MIN or 5MIN or 10MIN"})
                if not id:
                    return Response({"message":"user_id is required"})
                if id:
                    game = UserGameData.objects.filter(user_id_id=id , game_id__game_name= game_type).extra(
                select={
                    "winning_color_cleaned": '''replace(replace(replace(winning_color, '[', ''), ']', ''), "'", "")'''
                            }
                        ).values( "game_type", "amount", "type_of_bet", "bet" , "win_or_lose" , "winning_amount" , "winning_number", "winning_ball" , "created_at" , "game_id__game_type" ,'winning_color_cleaned')
                    return Response(game)
                game = UserGameData.objects.all().values()
                return Response(game)
            else:
                id = request.GET.get('id')
                game_type = request.GET.get('game_type')
                if id:
                    game = UserGameData.objects.filter(id=id).values()
                    # print(game)
                    # if not game_type or game_type not in ["1MIN","3MIN","5MIN","10MIN"]:
                    #     return Response({"message":"game_type is required and should be 1MIN or 3MIN or 5MIN or 10MIN"})
                    if not id:
                        return Response({"message":"user_id is required"})
                    if id:

                        game = UserGameData.objects.filter(user_id_id=id , game_id__game_type= game_type).extra(
                        select={
                            "winning_color_cleaned": '''replace(replace(replace(winning_color, '[', ''), ']', ''), "'", "")'''
                                    }
                                ).values( "game_type", "amount", "type_of_bet", "bet" , "win_or_lose" , "winning_amount" , "winning_number", "winning_ball" , "created_at" , "game_id__game_type" ,'winning_color_cleaned')
                        result = {}
                        overall_win = 0.0
                        win_or_lose = '-'
                        total_bet_amount = 0.0
                        # print(game,"sss")
                        if not game:
                            return Response('Game Not Found.')
                        for j in game:
                            if not j.get('winning_number') :
                                return Response('Game Not Found.')
                            result['winning_number'] = j['winning_number']
                            result['winning_ball'] = j['winning_ball']
                            result['winning_color'] = j['winning_color_cleaned']
                            total_bet_amount += j['amount'] if j.get('amount') else 0.0
                            overall_win += j['winning_amount'] if j.get('winning_amount') else 0.0
                        if overall_win >= total_bet_amount:
                            win_or_lose = "win"
                        else:
                            win_or_lose = "lose"
                        result['win_or_lose'] = win_or_lose
                        result['winning_amount'] = overall_win
                        result['total_bet_amount'] = total_bet_amount
                        return Response(result)
                    return Response("game_id is required")
        except Exception as e:
            return Response({"message":str(e)})



class GameClock(ListAPIView):
    def get(self,request):
        try:
            flag = request.GET.get('flag')
            if flag == "3":
                game_type , times = game_id_3min()
                return Response({"game_time":times,"game_id":game_type})
            elif flag == "5":
                game_type, time = game_id_5min()
                return Response({"game_time":time,"game_id":game_type})
            elif flag == "10":
                game_type, time = game_id_10min()
                return Response({"game_time":time,"game_id":game_type})
            else:
                game_type, time = game_id_1min()
                return Response({"game_time":time,"game_id":game_type})
            
        except Exception as e:
            return Response({"message":str(e)})
        
class UserPaymentHistory(ListAPIView):
    def get(self,request):
        try:
            id = request.GET.get('id')
            if id:
                user = UserPaymentModel.objects.filter(user_id=id).values()
                return Response(user)
            user = UserPaymentModel.objects.all().values()
            return Response({"data":user})
        except Exception as e:
            return Response({"message":str(e)})
        
class UserBankAPI(ListAPIView):
    def post(self,request):
        try:
            '''
            {
                "user_id":1,
                "account_number":"1234567890",
                "ifsc_code":"SBIN0000001",
                "bank_name":"SBI",
                "branch_name":"Delhi"
            }
            '''
            data = request.data
            if not data.get('user_id'):
                return Response({"message":"user_id is required"})
            user = UserDetail.objects.filter(id=data.get('user_id')).first()
            if user:
                UserBankDetails.objects.update_or_create(
                    
                    user_id = user,
                    defaults={
                        "account_number":data.get('account_number'),
                        "ifsc_code":data.get('ifsc_code'),
                        "bank_name":data.get('bank_name'),
                        "branch_name":data.get('branch_name')
                    }
                )
                return Response({"message":"Bank details added successfully"})
            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})
        
    def get(self,request):
        try:
            id = request.GET.get('id')
            if id:
                user = UserBankDetails.objects.filter(user_id=id).values()
                return Response(user)
            user = UserBankDetails.objects.all().values()
            return Response({"data":user})
        except Exception as e:
            return Response({"message":str(e)})
        
    def put(self,request):
        try:
            data = request.data
            user = UserDetail.objects.filter(id=data['user_id']).first()
            if user:
                bank = UserBankDetails.objects.filter(user_id=user).first()
                if bank:
                    bank.account_number = data.get('account_number')
                    bank.ifsc_code = data.get('ifsc_code')
                    bank.bank_name = data.get('bank_name')
                    bank.branch_name = data.get('branch_name')
                    bank.save()
                    return Response({"message":"Bank details updated successfully"})
                return Response({"message":"Bank details not found"})
            return Response({"message":"User not found"})
        except Exception as e:
            return Response({"message":str(e)})


class UserGameResultAPI(ListAPIView):
    def get(self,request):
        try:
            id = request.GET.get('id')
            game_id = request.GET.get('game_id')
            if id and game_id:
                game = UserGameData.objects.filter(user_id_id=id,game_id__game_type=game_id).values()
                return Response(game)
            return Response({"message":"id and game_id is required"})
        except Exception as e:
            return Response({"message":str(e)})
        
class UserwithdrawHistoryAPi(ListAPIView):
    def post(self,request):
        try:
            '''
            user_id: 100 
            amount : 200
            '''

            user_id = request.data.get('user_id')
            amount = request.data.get('amount')
            if not user_id or not amount:
                return Response({"message":"user_id and amount is required"})
            user_details = UserDetail.objects.filter(id= user_id).first()
            if user_details:
                if user_details.wallet >= amount:
                    user_bank_id = UserBankDetails.objects.filter( user_id=user_id).first()
                    if user_bank_id:
                        user_details.wallet  -= amount
                        user_details.save()
                        withdrawn_history = UserwithdrawHistory.objects.create(
                                user_id_id = user_details.id,
                                bank_id_id = user_bank_id.id,
                                status = 'In  Process',
                                amount = amount
                        )
                        return Response({"message": "Your Withdraw Request Is In Process.","transactionId":withdrawn_history.id} )
                    return ({"message": "bank details not fond."})
                return Response({"message": "Insufficient balance."})
            return Response({"message": "User does not exisits."}  )
        except Exception as e:
            return Response({"message":str(e)})
    
    def get(self,request):
        id = request.GET.get('user_id')
        if id:
            user_history = UserwithdrawHistory.objects.filter(user_id_id = id).values('id', 'user_id__username' , 'bank_id' , 'status' , 'amount' , 'created_at')
            return Response(user_history)
        return Response({"message": "User does not exisits."}  )

    
                             