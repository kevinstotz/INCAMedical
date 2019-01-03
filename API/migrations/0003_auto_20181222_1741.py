# Generated by Django 2.1.3 on 2018-12-22 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_customuser_user_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailtemplate',
            old_name='htmlFilename',
            new_name='html',
        ),
        migrations.RenameField(
            model_name='emailtemplate',
            old_name='textFilename',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='emailtemplate',
            name='fromAddress',
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='from_address',
            field=models.CharField(default='support@incamedical.com', max_length=50, verbose_name='Email Template From Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='creator',
            field=models.IntegerField(default=1, verbose_name='Email Template Creator'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='Email Template Owner'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='subject',
            field=models.CharField(max_length=60, verbose_name='Subject of Email Template'),
        ),
    ]
