# Generated by Django 2.2 on 2020-10-04 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradedata',
            name='price',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
