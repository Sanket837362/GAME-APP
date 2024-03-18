bet = [

    {
    
    
    "type_of_bet": "big/small",
    "bet": "small",
    "amount": 100,
    
} ,
{
    
    
    "type_of_bet": "color",
    "bet": "violet",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "color",
    "bet": "green",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "number",
    "bet": "6",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "number",
    "bet": "0",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "number",
    "bet": "2",
    "amount": 1000,
    
},
{
    
    
    "type_of_bet": "number",
    "bet": "8",
    "amount": 1000,
    
},
]

# def combile_same_bet(bet):
#     new_bet = []
#     for b in bet:
#         print(b)
#     # suppose bet is color and bet is green and amount is 1000 and there are 3 bets with same type and bet then combine them and make one bet with amount 3000 
#         if b['type_of_bet'] == "color" and b['bet'] in [x['bet'] for x in new_bet]:
#             for x in new_bet:
#                 if x['bet'] == b['bet']:
#                     x['amount'] += b['amount']
#         elif b['type_of_bet'] == "number" and b['bet'] in [x['bet'] for x in new_bet]:
#             for x in new_bet:
#                 if x['bet'] == b['bet']:
#                     x['amount'] += b['amount']
#         elif b['type_of_bet'] == "big/small" and b['bet'] in [x['bet'] for x in new_bet]:
#             for x in new_bet:
#                 if x['bet'] == b['bet']:
#                     x['amount'] += b['amount']
#         else:
#             new_bet.append(b)
#     return new_bet


# new_bet = combile_same_bet(bet)

# print(new_bet)
# print(bet)
def combine_same_bet(bet):
    combined_bets = {}
    
    for b in bet:
        key =  b['bet'] + b['type_of_bet']
        if key in combined_bets:
            combined_bets[key]['amount'] += b['amount']
        else:
            combined_bets[key] = {'type_of_bet': b['type_of_bet'], 'bet': b['bet'], 'amount': b['amount']}
    return list(combined_bets.values())

new_bet = combine_same_bet(bet)
print(new_bet)
