# Generated by Django 2.0.3 on 2020-08-29 00:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ablageort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ansicht',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Karte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('hinzugefuegt', models.DateField(default=datetime.date.today)),
                ('preis', models.FloatField()),
                ('bemerkung', models.CharField(max_length=500)),
                ('ablageort', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='karta.Ablageort')),
                ('gebiete', models.ManyToManyField(related_name='karten', to='karta.Gebiet')),
            ],
        ),
        migrations.CreateModel(
            name='Verlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Verlage',
                'ordering': ['anzahl_karten'],
            },
        ),
        migrations.CreateModel(
            name='Zweck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('beschreibung', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Zwecke',
            },
        ),
        migrations.AddField(
            model_name='karte',
            name='verlag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='karta.Verlag'),
        ),
        migrations.AddField(
            model_name='karte',
            name='zwecke',
            field=models.ManyToManyField(to='karta.Zweck'),
        ),
        migrations.AddField(
            model_name='ansicht',
            name='karte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='karta.Karte'),
        ),
        migrations.AddField(
            model_name='karte',
            name='laender',
            field=models.ManyToManyField(related_name='karten_in_land', to='karta.Land'),
        ),
        migrations.AddField(
            model_name='ansicht',
            name='koords_json',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='ansicht',
            name='massstab',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterModelOptions(
            name='ablageort',
            options={'verbose_name_plural': 'Ablageorte'},
        ),
        migrations.AlterModelOptions(
            name='ansicht',
            options={'verbose_name_plural': 'Ansichten'},
        ),
        migrations.AlterModelOptions(
            name='karte',
            options={'verbose_name_plural': 'Karten'},
        ),
        migrations.AddField(
            model_name='karte',
            name='stand',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='karte',
            name='bemerkung',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='ansicht',
            name='kurzbeschreibung',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='karte',
            name='reihenfolge',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='karte',
            name='hinzugefuegt',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='karte',
            name='preis',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='karte',
            name='ablageort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='karta.Ablageort'),
        ),
        migrations.AlterField(
            model_name='karte',
            name='verlag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='karta.Verlag'),
        ),
        migrations.RemoveField(
            model_name='karte',
            name='gebiete',
        ),
        migrations.RemoveField(
            model_name='karte',
            name='laender',
        ),
        migrations.CreateModel(
            name='Gebiet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Gebiete',
            },
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Länder',
            },
        ),
        migrations.AddField(
            model_name='gebiet',
            name='laender',
            field=models.ManyToManyField(blank=True, related_name='gebiete', to='karta.Land'),
        ),
        migrations.AddField(
            model_name='karte',
            name='gebiete',
            field=models.ManyToManyField(related_name='karten', to='karta'
                                                                   '.Gebiet'),
        ),
        migrations.AddField(
            model_name='karte',
            name='laender',
            field=models.ManyToManyField(related_name='karten_in_land', to='karta.Land'),
        ),
        migrations.AddField(
            model_name='karte',
            name='hat_gps',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='karte',
            name='hat_hoehenlinien',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='karte',
            name='hat_huelle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='karte',
            name='hat_ortsverzeichnis',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='karte',
            name='zustand',
            field=models.CharField(choices=[('N', 'Neu'), ('A', 'Alt')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='karte',
            name='verlag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='karta.Verlag'),
        ),
        migrations.AlterModelOptions(
            name='karte',
            options={'ordering': ['reihenfolge'], 'verbose_name_plural': 'Karten'},
        ),
        migrations.AlterField(
            model_name='ansicht',
            name='koords_json',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]