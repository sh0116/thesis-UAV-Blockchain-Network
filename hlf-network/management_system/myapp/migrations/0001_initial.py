# Generated by Django 4.1.7 on 2023-04-11 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import myapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('mission_name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('mission_coment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizations', models.TextField(blank=True)),
                ('peers', models.TextField(blank=True)),
                ('uavs', models.TextField(blank=True)),
                ('channels', models.TextField(blank=True)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('task_coment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('mission', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='myapp.mission')),
            ],
        ),
        migrations.AddField(
            model_name='mission',
            name='admin_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='mission', to='myapp.userprofile'),
        ),
        migrations.CreateModel(
            name='AuthenticationPeer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_name', models.TextField(blank=True)),
                ('mspid', models.TextField(blank=True)),
                ('cryptopath', models.TextField(blank=True, default='../management_system/media/')),
                ('peerendpoint', models.TextField(blank=True)),
                ('gatewaypeer', models.TextField(blank=True)),
                ('certpath', models.TextField(blank=True)),
                ('keypath', models.TextField(blank=True)),
                ('tlscertpath', models.TextField(blank=True)),
                ('keypath_file', models.FileField(blank=True, default='', upload_to=myapp.models.keypath_file_upload_to)),
                ('tlscertpath_file', models.FileField(blank=True, default='', upload_to=myapp.models.tlscertpath_file_upload_to)),
                ('certpath_file', models.FileField(blank=True, default='', upload_to=myapp.models.certpath_upload_to)),
                ('userprofile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Authprofile', to='myapp.userprofile')),
            ],
        ),
    ]
