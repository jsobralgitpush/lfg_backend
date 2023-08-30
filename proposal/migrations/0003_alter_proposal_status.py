# Generated by Django 4.2.4 on 2023-08-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_proposal_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('denied', 'Denied'), ('approved', 'Approved'), ('pending_by_system', 'Pending by system'), (
                'pending_by_user', 'Pending by user')], default='pending_by_system', max_length=20),
        ),
    ]