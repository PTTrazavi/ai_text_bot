# Generated by Django 2.2.4 on 2019-10-03 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Textupload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertext', models.TextField()),
                ('result', models.CharField(max_length=8)),
                ('date_of_upload', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]