# Generated by Django 2.2 on 2020-08-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.IntegerField(choices=[(1, 'To be done'), (2, 'In progress'), (3, 'Done')], default=1),
        ),
    ]