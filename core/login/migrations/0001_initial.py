# Generated by Django 5.0.6 on 2024-06-28 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mpId', models.IntegerField()),
                ('policialId', models.IntegerField()),
                ('data', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFim', models.TimeField()),
                ('status', models.CharField(max_length=50)),
                ('presente', models.BooleanField()),
            ],
        ),
    ]
