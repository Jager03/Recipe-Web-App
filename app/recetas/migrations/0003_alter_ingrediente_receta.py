# Generated by Django 4.1.1 on 2022-11-01 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_remove_receta_foto_fotoreceta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='receta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas', to='recetas.receta'),
        ),
    ]
