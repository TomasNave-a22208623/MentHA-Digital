# Generated by Django 4.0.5 on 2022-11-29 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0003_rename_materiais_exercicio_material_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respostas',
            old_name='sessaoGrupo',
            new_name='sessao_grupo',
        ),
        migrations.AddField(
            model_name='respostas',
            name='parte_grupo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='diario.partegrupo'),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='instrucao',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='instrucao_participante',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='material',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
