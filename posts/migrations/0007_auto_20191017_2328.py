# Generated by Django 2.2.6 on 2019-10-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20191017_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='file_id',
            field=models.FileField(max_length=200, upload_to=''),
        ),
    ]