# Generated by Django 3.2.15 on 2022-09-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_alter_review_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='star',
            field=models.PositiveIntegerField(blank=True, default=0, max_length=0.5),
        ),
    ]