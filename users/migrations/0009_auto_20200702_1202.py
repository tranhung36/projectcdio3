# Generated by Django 3.0.7 on 2020-07-02 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200702_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Mô tả'),
        ),
    ]
