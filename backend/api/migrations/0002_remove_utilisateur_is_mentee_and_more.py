# Generated by Django 4.2.13 on 2024-07-29 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='is_mentee',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='is_mentor',
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='status',
            field=models.CharField(choices=[('Mentor', 'Mentor'), ('Mentee', 'Mentee')], default='Mentee', max_length=6),
        ),
    ]
