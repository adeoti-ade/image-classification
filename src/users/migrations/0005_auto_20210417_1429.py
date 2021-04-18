# Generated by Django 2.2.18 on 2021-04-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210417_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email', 'username')},
        ),
    ]
