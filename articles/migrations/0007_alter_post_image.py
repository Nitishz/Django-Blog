# Generated by Django 3.2.8 on 2021-10-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_remove_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='thubmnails'),
        ),
    ]