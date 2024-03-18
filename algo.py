import random

def calculate_winning_number(bets):
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

    # Convert the array of bets into a dictionary
    bet = {}
    for b in bets:
        bet[b['type_of_bet']] = b['bet']
        bet[b['type_of_bet'] + '_amount'] = b['amount']

    # Calculate the total bet amount
    total_bet_amount = sum([b['amount'] for b in bets])

    # Create a weighted list of potential winning numbers
    potential_winning_numbers = []
    for number, attributes in color_and_number_of_balls.items():
        if 'big' in attributes and 'big/small' in bet and bet['big/small'] == 'big':
            potential_winning_numbers.append(number)
        if 'small' in attributes and 'big/small' in bet and bet['big/small'] == 'small':
            potential_winning_numbers.append(number)
        if 'green' in attributes and 'color' in bet and bet['color'] == 'green':
            potential_winning_numbers.append(number)
        if 'red' in attributes and 'color' in bet and bet['color'] == 'red':
            potential_winning_numbers.append(number)
        if 'violet' in attributes and 'color' in bet and bet['color'] == 'violet':
            potential_winning_numbers.append(number)
        if number == bet.get('number'):
            potential_winning_numbers.append(number)

    # Randomly select a winning number from the weighted list
    winning_number = random.choice(potential_winning_numbers)

    # Calculate the winning amount
    winning_amount = 0
    if winning_number == bet.get('number'):
        winning_amount += 8 * bet.get('number_amount', 0) 
    if color_and_number_of_balls[winning_number][0] == bet.get('color'):
        if bet.get('color') == 'red' and winning_number == '0':
            winning_amount += 1.5 * bet.get('color_amount', 0)
        elif bet.get('color') == 'green' and winning_number == '5':
            winning_amount += 1.5 * bet.get('color_amount', 0)
        elif bet.get('color') == 'violet':
            winning_amount += 4.5 * bet.get('color_amount', 0)
        else:
            winning_amount += 2 * bet.get('color_amount', 0)
    if 'big' in color_and_number_of_balls[winning_number] and 'big/small' in bet and bet['big/small'] == 'big':
        winning_amount += 2 * bet.get('big/small_amount', 0)
    if 'small' in color_and_number_of_balls[winning_number] and 'big/small' in bet and bet['big/small'] == 'small':
        winning_amount += 2 * bet.get('big/small_amount', 0)

    # Ensure the winning amount is always less than the total bet amount
    if winning_amount > total_bet_amount:
        return calculate_winning_number(bets)
    # return the winning number, the winning amount, total bet amount , color of the ball can be multiple and
    return winning_number, winning_amount , total_bet_amount , ",".join(color_and_number_of_balls[winning_number][0:-1]) , color_and_number_of_balls[winning_number][-1]

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
    "bet": "red",
    "amount": 1000,
    "user_id": "user1"
},
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "3",
    "amount": 100,
    "user_id": "user1"
},
]

winning_number, winning_amount , total_bet_amount , color , ball = calculate_winning_number(bet)
print(f"The winning number is {winning_number} color of the ball is {color} and the ball is {ball} and the winning amount is {winning_amount} and the total bet amount is {total_bet_amount}")
# make a list of all the bets and then calculate the winning number and the winning amount for each bet

outputs = []
sum_of_all_bets_winning_amount = 0
for vals in bet:
    if vals['type_of_bet'] == "big/small":
        if ball == vals['bet']:
            user_winning_amount = 2 * vals['amount']
            sum_of_all_bets_winning_amount += user_winning_amount
            outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
    elif vals['type_of_bet'] == "color":
            print(vals['bet'] , color , vals['bet'] == "red" , "red" in color)
            if "violet" in color and vals['bet'] == "violet":
                user_winning_amount = 4.5 * vals['amount']
                sum_of_all_bets_winning_amount += user_winning_amount
                outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
            elif "red" in color and vals['bet'] == "red":
                if winning_number == "0":
                    user_winning_amount = 1.5 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
                else:
                    user_winning_amount = 2 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
            elif "green" in color and vals['bet'] == "green":
                if winning_number == "5":
                    user_winning_amount = 1.5 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
                else:
                    user_winning_amount = 2 * vals['amount']
                    sum_of_all_bets_winning_amount += user_winning_amount
                    outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})
                    
    elif vals['type_of_bet'] == "number":
        if winning_number == vals['bet']:
            user_winning_amount = 8 * vals['amount']
            sum_of_all_bets_winning_amount += user_winning_amount
            outputs.append({"type_of_bet":vals['type_of_bet'],"winning_amount":user_winning_amount,"bet_amount":vals['amount']})

print(outputs)
print(f"The sum of all the bets winning amount is {sum_of_all_bets_winning_amount}" , "and the winning amount from algo ",winning_amount)
if sum_of_all_bets_winning_amount <= winning_amount:
    print("Pass the test case")
else:
    print("Fail the test case")
    raise Exception("The sum of all the bets winning amount is greater than the winning amount")
    
    





'''

The winning number is 0 color of the ball is red,violet and the ball is small and the winning amount is 1700.0 and the total bet amount is 2200
violet red,violet False True
red red,violet True True
[{'type_of_bet': 'big/small', 'winning_amount': 200, 'bet_amount': 100}, {'type_of_bet': 'color', 'winning_amount': 4500.0, 'bet_amountcolor', 'winning_amount': 1500.0, 'bet_amount': 1000}]
The sum of all the bets winning amount is 6200.0 and the winning amount from algo  1700.0
Fail the test case
Traceback (most recent call last):
  File "D:\Python Project\Game App\game_site\algo.py", line 154, in <module>
    raise Exception("The sum of all the bets winning amount is greater than the winning amount")
Exception: The sum of all the bets winning amount is greater than the winning amount
failde due to violet color 

'''