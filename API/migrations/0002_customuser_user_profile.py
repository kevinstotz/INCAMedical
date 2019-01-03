# Generated by Django 2.1.3 on 2018-12-22 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customUserUserProfile', to='API.UserProfile', verbose_name='Custom User User Profile'),
        ),
    ]