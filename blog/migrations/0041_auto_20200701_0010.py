# Generated by Django 3.0.7 on 2020-06-30 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_auto_20200630_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='post_pics', verbose_name='images')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=None, upload_to='post_pics', verbose_name='image'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
