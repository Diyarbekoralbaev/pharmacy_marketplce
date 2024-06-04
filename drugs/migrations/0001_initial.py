# Generated by Django 5.0.6 on 2024-06-03 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(default='images/drugs/default.jpg', upload_to='images/drugs')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]