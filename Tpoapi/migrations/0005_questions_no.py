# Generated by Django 4.2.5 on 2024-04-03 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tpoapi', '0004_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='no',
            field=models.PositiveIntegerField(null=True),
        ),
    ]