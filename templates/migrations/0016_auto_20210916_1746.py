# Generated by Django 3.1.6 on 2021-09-16 17:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0015_attributeoption_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
