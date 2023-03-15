# Generated by Django 4.1.3 on 2023-03-15 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassActivity',
            fields=[
                ('week_id', models.IntegerField(max_length=4, primary_key=True, serialize=False)),
                ('tracking_video', models.CharField(max_length=1024)),
                ('credit_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.creditclass')),
            ],
        ),
    ]
