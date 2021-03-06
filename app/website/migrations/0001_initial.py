# Generated by Django 3.2.7 on 2021-11-11 20:29

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(default='', max_length=100, verbose_name='Full name')),
                ('avatar', models.ImageField(upload_to='uploads/avatars/', verbose_name='Avatar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('image', models.ImageField(upload_to='uploads/talks/', verbose_name='Imagen')),
                ('is_draft', models.BooleanField(default=True, verbose_name='¿Es un borrador?')),
                ('content', tinymce.models.HTMLField(verbose_name='Contenido')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Creado')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to='website.profile', verbose_name='Autor')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Categoría', to='website.category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Charla',
                'verbose_name_plural': 'Charlas',
                'ordering': ('-created_at',),
            },
        ),
    ]
