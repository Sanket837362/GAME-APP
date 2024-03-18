import random
import random

def calculate_winning_number(bet):
    color_and_number_of_balls = {
        "0": [ 'red', 'violet','small' ],
        "1": [ 'green','small' ],
        "2": [ 'red' ,'small'],
        "3": [ 'green' ,'small'],
        "4": [ 'red' ,'small'],
        "5": [ 'green', 'violet','big' ],
        "6": [ 'red' ,'big'],
        "7": [ 'green' ,'big'],
        "8": [ 'red' ,'big'],
        "9": [ 'green' ,'big']
    }
    
    amount = sum([b['amount'] for b in bet])
    winning_amount = amount * 0.98  # 90% of total betting amount
    print(winning_amount)
    
    while True:
        winning_number = str(random.randint(0, 9))
        ball = color_and_number_of_balls[winning_number]
        amount = 0
        for b in bet:
            if b['type_of_bet'] == 'big/small' and b['bet'] == ball[-1]:
                amount += b['amount'] * 2
            elif b['type_of_bet'] == 'color' and b['bet'] in ball[0:-1]:
                amount += b['amount'] * 2 if b['bet'] != 'violet' else b['amount'] * 4.5
            elif b['type_of_bet'] == 'number' and str(b['bet']) == str(winning_number):
                amount += b['amount'] * 8        
        
        if amount <= winning_amount:
            print(amount)
            break
    print(winning_number, winning_amount , amount , ball[0:-1] , ball[-1])
    return winning_number, winning_amount , amount , ball[0:-1] , ball[-1]

bet = [

    {
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "big/small",
    "bet": "small",
    "amount": 100,
    "user_id": "user1"
} ,
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "violet",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "6",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "0",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "2",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "8",
    "amount": 1000,
    "user_id": "user1"
},
]
# bet = [{'type_of_bet': 'big/small', 'bet': 'big', 'amount': 600}, {'type_of_bet': 'color', 'bet': 'red', 'amount': 600}, {'type_of_bet': 'number', 'bet': '1', 'amount': 200}]
# bet = []
winning_number,total_bet_amount, winning_amount ,   color , ball = calculate_winning_number(bet)
print(winning_number,  total_bet_amount ,winning_amount, color , ball)

outputs = []
sum_of_all_bets_winning_amount = 0
for vals in bet:
    if vals['type_of_bet'] == "big/small":
        if ball == vals['bet']:
            user_winning_amount = 2 * vals['amount']
            sum_of_all_bets_winning_amount += user_winning_amount
            outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})
    elif vals['type_of_bet'] == "color":
            if "violet" in color and vals['bet'] == "violet":
                user_winning_amount = 4.5 * vals['amount']
                sum_of_all_bets_winning_amount += user_winning_amount
                outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})
            elif "red" in color and vals['bet'] == "red":
                if winning_number == "0":
                    user_winning_amount = 1.5 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})
                else:
                    user_winning_amount = 2 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})
            elif "green" in color and vals['bet'] == "green":
                if winning_number == "5":
                    user_winning_amount = 1.5 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})
                else:
                    user_winning_amount = 2 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})

    elif vals['type_of_bet'] == "number":
        if winning_number == vals['bet']:
            user_winning_amount = 8 * vals['amount']
            sum_of_all_bets_winning_amount += user_winning_amount
            outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount'] , "winning_number":winning_number , "selected_bet":vals['bet']})

print(outputs)
print(f"The sum of all the bets winning amount is {sum_of_all_bets_winning_amount}" , "and the winning amount from algo ",winning_amount)
if sum_of_all_bets_winning_amount <= winning_amount:
    print("Pass the test case")
else:
    print("Fail the test case")
    raise Exception("The sum of all the bets winning amount is greater than the winning amount")




