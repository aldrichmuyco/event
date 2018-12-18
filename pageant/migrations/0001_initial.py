# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 16:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
                ('maximum_score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CriteriaCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pageant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PageantParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('deduction', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PageantParticipantRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.Criteria')),
                ('judge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.Judge')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.PageantParticipant')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pageant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.Pageant')),
            ],
        ),
        migrations.AddField(
            model_name='pageantparticipant',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.ParticipantGroup'),
        ),
        migrations.AddField(
            model_name='judge',
            name='pageant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.Pageant'),
        ),
        migrations.AddField(
            model_name='judge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='criteriacategory',
            name='pageant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.Pageant'),
        ),
        migrations.AddField(
            model_name='criteria',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pageant.CriteriaCategory'),
        ),
    ]
