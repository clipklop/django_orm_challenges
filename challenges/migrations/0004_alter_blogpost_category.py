# Generated by Django 4.2.3 on 2023-10-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.CharField(choices=[('general', 'general'), ('programming', 'programming'), ('sport', 'sport'), ('food', 'food')], default=None, max_length=50),
        ),
    ]
