# Generated by Django 2.2.4 on 2019-10-15 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=64)),
                ('contact', models.CharField(max_length=16)),
                ('phone', models.CharField(max_length=16)),
                ('fax', models.CharField(max_length=16)),
                ('usertext', models.TextField()),
                ('message', models.TextField()),
                ('date_of_inquiry', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]