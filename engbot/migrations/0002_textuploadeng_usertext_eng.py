# Generated by Django 2.2.4 on 2020-03-27 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textuploadeng',
            name='usertext_eng',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
