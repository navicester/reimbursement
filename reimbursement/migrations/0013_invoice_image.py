# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-10 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0012_approvalrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'invoice/image', verbose_name='image'),
        ),
    ]
