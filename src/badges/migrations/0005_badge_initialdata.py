# Generated by Django 2.2.12 on 2020-05-09 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0004_badgetype_initialdata'),
    ]

    operations = [
        #migrations.RunPython(load_initial_data),
        # For some reason having this before 0008 was causing error: cannot DROP TABLE "badges_badge" because it has pending trigger events
        # so duplicated in 0009
    ]
