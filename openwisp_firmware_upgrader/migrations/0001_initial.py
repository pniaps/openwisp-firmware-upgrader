# Generated by Django 2.0.5 on 2018-05-11 16:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import openwisp_users.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('config', '0012_auto_20180219_1501'),
        ('openwisp_users', '0002_auto_20180508_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('version', models.CharField(db_index=True, max_length=32)),
                ('changelog', models.TextField(blank=True, help_text='descriptive text indicating what has changed since the previous version, if applicable', verbose_name='change log')),
            ],
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField(blank=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DeviceFirmware',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('installed', models.BooleanField(default=False)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='config.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FirmwareImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to='')),
                ('models', models.TextField(blank=True, help_text='hardware models this image refers to, one per line')),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firmware_upgrader.Build')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization')),
            ],
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UpgradeOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('in-progress', 'in progress'), ('success', 'success'), ('failed', 'failed'), ('aborted', 'aborted')], default='in-progress', max_length=12)),
                ('log', models.TextField(blank=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Device')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firmware_upgrader.FirmwareImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='devicefirmware',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firmware_upgrader.FirmwareImage'),
        ),
        migrations.AddField(
            model_name='build',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firmware_upgrader.Category'),
        ),
        migrations.AddField(
            model_name='build',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='build',
            name='previous',
            field=models.ForeignKey(blank=True, help_text='previous version of this build', null=True, on_delete=django.db.models.deletion.SET_NULL, to='firmware_upgrader.Build', verbose_name='previous build'),
        ),
        migrations.AlterUniqueTogether(
            name='firmwareimage',
            unique_together={('build', 'models')},
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together={('category', 'version')},
        ),
    ]
