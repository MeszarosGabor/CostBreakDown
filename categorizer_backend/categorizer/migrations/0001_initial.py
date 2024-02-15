# Generated by Django 4.2.2 on 2023-12-18 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.TextField(unique=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('merchant', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
