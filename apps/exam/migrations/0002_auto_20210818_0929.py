# Generated by Django 3.2.6 on 2021-08-18 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='duration',
            field=models.PositiveIntegerField(default=60, help_text='Duration in minutes. 60 means 60 minutes/1 hour.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='exam/questions/audio/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='exam/questions/images/'),
        ),
        migrations.AlterField(
            model_name='questionchoice',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='exam/choices/audio/'),
        ),
        migrations.AlterField(
            model_name='questionchoice',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='exam/choices/images/'),
        ),
    ]
