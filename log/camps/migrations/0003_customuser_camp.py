# Generated by Django 5.1.3 on 2024-11-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0002_remove_customuser_camp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='camp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
