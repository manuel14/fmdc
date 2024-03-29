# Generated by Django 2.1.15 on 2022-07-12 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0077_alter_actividad_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('link', models.FileField(default='', upload_to='files/', verbose_name='Archivo')),
                ('act', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Actividad')),
            ],
            options={
                'verbose_name': 'Archivo',
                'verbose_name_plural': 'Archivos',
            },
        ),
    ]
