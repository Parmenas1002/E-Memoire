# Generated by Django 3.2 on 2015-09-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_memoire_academicyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoire',
            name='academicYear',
            field=models.CharField(choices=[('2014-2015', '2014-2015')], default='2014-2015', max_length=20, verbose_name='Année Académique'),
        ),
    ]
