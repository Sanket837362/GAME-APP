from django.db import models

# Create your models here.

class UserDetail(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50 , null = True , blank = True)
    phone = models.CharField(max_length=10 , null = True , blank = True)
    wallet = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class UserPaymentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    amount = models.FloatField()
    upi_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class GameDetail(models.Model):
    id = models.AutoField(primary_key=True)
    game_type = models.CharField(max_length=50)
    game_name = models.CharField(max_length=50)
    game_description = models.TextField()
    result = models.CharField(max_length=50)
    ball = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserGameData(models.Model):
    id = models.AutoField(primary_key=True)
    game_type = models.CharField(max_length=50)
    game_id = models.ForeignKey(GameDetail,on_delete=models.CASCADE)
    type_of_bet = models.CharField(max_length=50)
    bet = models.CharField(max_length=50)
    amount = models.FloatField()
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    win_or_lose = models.CharField(max_length=50 , null = True , blank = True)
    winning_amount = models.FloatField(null = True , blank = True)
    winning_number = models.CharField(max_length=50 , null = True , blank = True)
    winning_color = models.CharField(max_length=50 , null = True , blank = True)
    winning_ball = models.CharField(max_length=50 , null = True , blank = True)


class liveUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=50)
    flag = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class result(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(GameDetail, on_delete=models.CASCADE, related_name='game_results' )
    game_type = models.CharField(max_length=50)
    winning_number = models.CharField(max_length=50)
    winning_color = models.CharField(max_length=50)
    winning_ball = models.CharField(max_length=50)
    total_bet_amount = models.FloatField()
    total_win_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserBankDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserwithdrawHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    bank_id = models.ForeignKey(UserBankDetails,on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 

class Userdeposithistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=50)
    utr_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 