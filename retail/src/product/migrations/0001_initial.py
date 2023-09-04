# Generated by Django 4.2.5 on 2023-09-04 15:44

import core.models
import cuid2.generator
from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', core.models.CuidField(default=cuid2.generator.Cuid.generate, editable=False, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('name', models.TextField()),
                ('slug', models.TextField()),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
            bases=(models.Model, product.models.SlugMixin),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', core.models.CuidField(default=cuid2.generator.Cuid.generate, editable=False, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('is_available_for_purchase', models.BooleanField(default=True)),
                ('name', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seller', core.models.CuidField(default=cuid2.generator.Cuid.generate, max_length=12)),
                ('slug', models.TextField()),
                ('categories', models.ManyToManyField(related_name='products', to='product.category')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
            bases=(models.Model, product.models.SlugMixin),
        ),
    ]
