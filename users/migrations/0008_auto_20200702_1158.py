# Generated by Django 3.0.7 on 2020-07-02 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, verbose_name='Mô tả'),
        ),
    ]
