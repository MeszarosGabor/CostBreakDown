# Generated by Django 4.2.2 on 2023-12-18 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorizer', '0003_categorizedtransaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorizedtransaction',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='categorized_transactions', to='categorizer.transaction'),
        ),
    ]