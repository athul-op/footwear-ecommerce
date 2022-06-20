# Generated by Django 3.2.13 on 2022-06-04 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='images/product')),
                ('description', models.TextField(max_length=1000)),
                ('available', models.BooleanField(default=True, verbose_name='available')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
