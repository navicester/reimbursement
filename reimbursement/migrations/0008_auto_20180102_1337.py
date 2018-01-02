# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-02 05:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reimbursement', '0007_auto_20171227_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='current approver')),
                ('prev_approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reimbursement.ApprovalChain', verbose_name='prev approver')),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.CharField(choices=[(b'RMB', 'RMB'), (b'USD', 'USD'), (b'EUR', 'EUR')], max_length=30, verbose_name='currency'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(choices=[(b'ordinary', 'ordinary VAT invoice'), (b'special', 'special invoice'), (b'notinvoice', 'not invoice')], max_length=30, verbose_name='invoice type'),
        ),
    ]
