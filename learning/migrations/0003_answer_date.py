# Generated by Django 2.2.12 on 2020-05-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("learning", "0002_auto_20200511_1705")]

    operations = [
        migrations.AddField(
            model_name="answer", name="date", field=models.DateField(blank=True, null=True)
        )
    ]
