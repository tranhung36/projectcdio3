# Generated by Django 3.0.7 on 2020-06-30 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0043_auto_20200701_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default=None, upload_to='post_pics', verbose_name='image'),
        ),
    ]
