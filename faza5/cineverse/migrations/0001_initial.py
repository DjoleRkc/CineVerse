# Generated by Django 5.0.6 on 2024-05-30 19:09

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uloga', models.CharField(max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'nalog',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('idfil', models.AutoField(db_column='idFil', primary_key=True, serialize=False)),
                ('naziv', models.CharField(max_length=45)),
                ('originalninaziv', models.CharField(db_column='originalniNaziv', max_length=45)),
                ('trajanje', models.IntegerField()),
                ('pocetakprikazivanja', models.DateField(db_column='pocetakPrikazivanja')),
                ('reziseri', models.CharField(max_length=100)),
                ('glumci', models.CharField(max_length=150)),
                ('krataksadrzaj', models.CharField(db_column='kratakSadrzaj', max_length=150)),
                ('radnja', models.CharField(max_length=500)),
                ('ocenaimdb', models.FloatField(db_column='ocenaIMDB')),
                ('ocenakorisnika', models.FloatField(db_column='ocenaKorisnika')),
                ('slika', models.CharField(max_length=1000)),
                ('sredjennaziv', models.CharField(db_column='sredjenNaziv', default='', max_length=45)),
            ],
            options={
                'db_table': 'film',
            },
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('idsal', models.AutoField(db_column='idSal', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'sala',
            },
        ),
        migrations.CreateModel(
            name='Termin',
            fields=[
                ('idter', models.AutoField(db_column='idTer', primary_key=True, serialize=False)),
                ('termin', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'termin',
            },
        ),
        migrations.CreateModel(
            name='Zanr',
            fields=[
                ('idzan', models.AutoField(db_column='idZan', primary_key=True, serialize=False)),
                ('naziv', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'zanr',
            },
        ),
        migrations.CreateModel(
            name='Projekcija',
            fields=[
                ('idpro', models.AutoField(db_column='idPro', primary_key=True, serialize=False)),
                ('datum', models.CharField(max_length=100)),
                ('idfil', models.ForeignKey(db_column='idFil', on_delete=django.db.models.deletion.CASCADE, to='cineverse.film')),
                ('idsal', models.ForeignKey(db_column='idSal', on_delete=django.db.models.deletion.CASCADE, to='cineverse.sala')),
                ('idter', models.ForeignKey(db_column='idTer', on_delete=django.db.models.deletion.CASCADE, to='cineverse.termin')),
            ],
            options={
                'db_table': 'projekcija',
            },
        ),
        migrations.CreateModel(
            name='Sediste',
            fields=[
                ('idsed', models.IntegerField(db_column='idSed', primary_key=True, serialize=False)),
                ('red', models.IntegerField()),
                ('kolona', models.CharField(max_length=1)),
                ('idsal', models.ForeignKey(db_column='idSal', on_delete=django.db.models.deletion.CASCADE, to='cineverse.sala')),
            ],
            options={
                'db_table': 'sediste',
            },
        ),
        migrations.CreateModel(
            name='Rezervacija',
            fields=[
                ('idrez', models.AutoField(db_column='idRez', primary_key=True, serialize=False)),
                ('idkor', models.ForeignKey(db_column='idKor', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idpro', models.ForeignKey(db_column='idPro', on_delete=django.db.models.deletion.CASCADE, to='cineverse.projekcija')),
                ('idsed', models.ForeignKey(db_column='idSed', on_delete=django.db.models.deletion.CASCADE, to='cineverse.sediste')),
            ],
            options={
                'db_table': 'rezervacija',
            },
        ),
        migrations.CreateModel(
            name='Predlaze',
            fields=[
                ('idkor', models.OneToOneField(db_column='idKor', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nazivfilma', models.CharField(db_column='nazivFilma', max_length=200)),
            ],
            options={
                'db_table': 'predlaze',
                'unique_together': {('idkor', 'nazivfilma')},
            },
        ),
        migrations.CreateModel(
            name='Ocenjuje',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ocena', models.IntegerField()),
                ('idfil', models.ForeignKey(db_column='idFil', on_delete=django.db.models.deletion.CASCADE, to='cineverse.film')),
                ('idkor', models.OneToOneField(db_column='idKor', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ocenjuje',
                'unique_together': {('idkor', 'idfil')},
            },
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idfil', models.ForeignKey(db_column='idFil', on_delete=django.db.models.deletion.CASCADE, to='cineverse.film')),
                ('idkor', models.OneToOneField(db_column='idKor', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'watchlist',
                'unique_together': {('idkor', 'idfil')},
            },
        ),
        migrations.CreateModel(
            name='ImaZanr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idfil', models.OneToOneField(db_column='idFil', on_delete=django.db.models.deletion.CASCADE, to='cineverse.film')),
                ('idzan', models.ForeignKey(db_column='idZan', on_delete=django.db.models.deletion.CASCADE, to='cineverse.zanr')),
            ],
            options={
                'db_table': 'ima_zanr',
                'unique_together': {('idfil', 'idzan')},
            },
        ),
    ]
