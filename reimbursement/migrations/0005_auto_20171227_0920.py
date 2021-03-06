# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-27 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0004_auto_20171222_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_status',
            field=models.CharField(choices=[(b'notsubmitted', 'not submitted'), (b'inprogress', 'in progress'), (b'approved', 'approved')], default=b'notsubmitted', max_length=30, verbose_name='invoice status'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_category',
            field=models.CharField(choices=[(b'1', 'Operation'), (b'2', 'Market'), (b'3', 'R&D')], max_length=30, verbose_name='invoice category'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_project',
            field=models.CharField(choices=[(b'1', 'Meals'), (b'2', 'Rent'), (b'3', 'Travel')], max_length=30, verbose_name='invoice project'),
        ),
    ]
