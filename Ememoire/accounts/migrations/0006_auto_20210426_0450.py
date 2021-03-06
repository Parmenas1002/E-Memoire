# Generated by Django 3.2 on 2021-04-26 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_lmemoire_student_memoire'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='memoire',
            name='abstract',
            field=models.TextField(blank=True, null=True, verbose_name='Résumé du Mémoire'),
        ),
        migrations.AlterField(
            model_name='memoire',
            name='stateAfter',
            field=models.BooleanField(default=False, verbose_name='Statut après la soutenance'),
        ),
    ]
