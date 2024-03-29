# Generated by Django 4.2.2 on 2023-12-18 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorizer', '0002_category_categorypattern_categorizedtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorizedtransaction',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categorized_transactions', to='categorizer.category'),
        ),
    ]
