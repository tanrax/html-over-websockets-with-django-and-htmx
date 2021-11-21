# Generated by Django 3.2.9 on 2021-11-21 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20211121_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talkcategory', to='website.category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='speaker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talkspeaker', to='website.profile', verbose_name='Ponente'),
        ),
    ]