# Generated by Django 4.2.11 on 2024-04-03 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0006_remove_gamedetail_new_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userdeposithistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('upi_id', models.CharField(max_length=50)),
                ('utr_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_registration.userdetail')),
            ],
        ),
    ]
