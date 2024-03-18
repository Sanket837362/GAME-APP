import random

def calculate_all_outcomes(bets):
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

    # Calculate all possible outcomes
    outcomes = []
    for number, attributes in color_and_number_of_balls.items():
        winning_amount = 0
        if number == bet.get('number'):
            winning_amount += 8 * bet.get('number_amount', 0)
        if color_and_number_of_balls[number][0] == bet.get('color'):
            if bet.get('color') == 'red' and number == '0':
                winning_amount += 1.5 * bet.get('color_amount', 0)
            elif bet.get('color') == 'green' and number == '5':
                winning_amount += 1.5 * bet.get('color_amount', 0)
            elif bet.get('color') == 'violet':
                winning_amount += 4.5 * bet.get('color_amount', 0)
            else:
                winning_amount += 2 * bet.get('color_amount', 0)
        if 'big' in color_and_number_of_balls[number] and 'big/small' in bet and bet['big/small'] == 'big':
            winning_amount += 2 * bet.get('big/small_amount', 0)
        if 'small' in color_and_number_of_balls[number] and 'big/small' in bet and bet['big/small'] == 'small':
            winning_amount += 2 * bet.get('big/small_amount', 0)

        outcomes.append({
            'winning_number': number,
            'total_bet_amount': total_bet_amount,
            'winning_amount': winning_amount
        })

    return outcomes

bet = [

    {
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "big/small",
    "bet": "big",
    "amount": 100,
    "user_id": "user1"
} ,
{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "color",
    "bet": "violet",
    "amount": 100,
    "user_id": "user1"
},

{
    "game_type": "1 minute",
    "game_id": "1MIN20240316152211",
    "type_of_bet": "number",
    "bet": "5",
    "amount": 100,
    "user_id": "user1"
},
]

print(calculate_all_outcomes(bet))