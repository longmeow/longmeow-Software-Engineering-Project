# Generated by Django 4.1.3 on 2023-03-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_alter_classactivity_week_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classactivity',
            name='video_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classactivity',
            name='week_id',
            field=models.IntegerField(),
        ),
    ]
