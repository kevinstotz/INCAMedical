# Generated by Django 2.1.3 on 2018-11-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicatortype',
            name='type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='indicatortype',
            unique_together={('company', 'type')},
        ),
    ]