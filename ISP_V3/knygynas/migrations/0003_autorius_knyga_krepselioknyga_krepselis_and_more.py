# Generated by Django 4.2.16 on 2024-12-20 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knygynas', '0002_rename_complete_todoitem_completed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorius',
            fields=[
                ('id_Autorius', models.AutoField(primary_key=True, serialize=False)),
                ('vardas', models.CharField(max_length=255)),
                ('pavarde', models.CharField(max_length=255)),
                ('gimimo_metai', models.DateField()),
            ],
            options={
                'db_table': 'autoriai',
            },
        ),
        migrations.CreateModel(
            name='Knyga',
            fields=[
                ('id_Knyga', models.AutoField(primary_key=True, serialize=False)),
                ('kaina', models.FloatField()),
                ('leidimo_metai', models.DateField()),
                ('aprasymas', models.CharField(blank=True, max_length=255, null=True)),
                ('likutis', models.IntegerField()),
                ('pavadinimas', models.CharField(max_length=255)),
                ('akcija', models.FloatField(blank=True, null=True)),
                ('akcijos_galiojimas', models.DateField(blank=True, null=True)),
                ('uzsaldyta', models.BooleanField()),
                ('virselio_tipas', models.CharField(choices=[('kietas', 'Kietas'), ('minkštas', 'Minkštas')], max_length=8)),
                ('fk_Autorius', models.ForeignKey(db_column='fk_Autorius', on_delete=django.db.models.deletion.CASCADE, to='knygynas.autorius')),
            ],
            options={
                'db_table': 'knygos',
            },
        ),
        migrations.CreateModel(
            name='KrepselioKnyga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fk_Knyga', models.ForeignKey(db_column='fk_Knyga', on_delete=django.db.models.deletion.CASCADE, to='knygynas.knyga')),
            ],
            options={
                'db_table': 'krepselio_knyga',
            },
        ),
        migrations.CreateModel(
            name='Krepselis',
            fields=[
                ('id_Krepselis', models.AutoField(primary_key=True, serialize=False)),
                ('bendra_kaina', models.FloatField()),
                ('kiekis', models.IntegerField()),
                ('PVM', models.FloatField()),
                ('uzsakymo_data', models.DateField()),
                ('planuojama_pristatymo_data', models.DateField()),
                ('uzsakymo_busena', models.CharField(max_length=255)),
                ('sekimo_numeris', models.CharField(max_length=255)),
                ('gavejo_adresas', models.CharField(max_length=255)),
                ('issiuntimo_data', models.DateField()),
                ('gavimo_data', models.DateField()),
                ('valiuta', models.CharField(choices=[('euras', 'Euras'), ('doleris', 'Doleris'), ('svaras', 'Svaras')], max_length=7)),
            ],
            options={
                'db_table': 'krepseliai',
            },
        ),
        migrations.CreateModel(
            name='Kurjerio_Knygos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'kurjerio_knygos',
            },
        ),
        migrations.CreateModel(
            name='Kurjeris',
            fields=[
                ('id_Kurjeris', models.AutoField(primary_key=True, serialize=False)),
                ('pavadinimas', models.CharField(max_length=255)),
                ('tel_numeris', models.CharField(max_length=255)),
                ('el_pastas', models.CharField(max_length=255)),
                ('transporto_priemones_tipas', models.CharField(blank=True, max_length=255, null=True)),
                ('paslaugu_teikimo_teritorija', models.CharField(max_length=255)),
                ('reitingas', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'kurjeriai',
            },
        ),
        migrations.CreateModel(
            name='Leidykla',
            fields=[
                ('id_Leidykla', models.AutoField(primary_key=True, serialize=False)),
                ('pavadinimas', models.CharField(max_length=255)),
                ('adresas', models.CharField(max_length=255)),
                ('ikurimo_data', models.DateField()),
            ],
            options={
                'db_table': 'leidyklos',
            },
        ),
        migrations.CreateModel(
            name='PrekiuUzsakymas',
            fields=[
                ('id_Prekiu_uzsakymas', models.AutoField(primary_key=True, serialize=False)),
                ('knygu_kiekis', models.IntegerField()),
                ('uzsakymo_data', models.DateField()),
                ('issiuntimo_data', models.DateField()),
                ('atvykimo_data', models.DateField()),
                ('prekiu_busena', models.CharField(choices=[('užsakyta', 'Užsakyta'), ('atvyksta', 'Atvyksta'), ('įvykdyta', 'Įvykdyta'), ('atšaukta', 'Atšaukta'), ('grąžinama', 'Grąžinama')], max_length=9)),
            ],
            options={
                'db_table': 'prekiu_uzsakymai',
            },
        ),
        migrations.CreateModel(
            name='SandelioKnygos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fk_Knyga', models.ForeignKey(db_column='fk_Knyga', on_delete=django.db.models.deletion.CASCADE, to='knygynas.knyga')),
            ],
            options={
                'db_table': 'sandelio_knygos',
            },
        ),
        migrations.CreateModel(
            name='Sandelis',
            fields=[
                ('id_Sandelis', models.AutoField(primary_key=True, serialize=False)),
                ('adresas', models.CharField(max_length=255)),
                ('inventorius', models.IntegerField()),
                ('talpa', models.IntegerField()),
            ],
            options={
                'db_table': 'sandeliai',
            },
        ),
        migrations.CreateModel(
            name='Saskaita',
            fields=[
                ('id_Saskaita', models.AutoField(primary_key=True, serialize=False)),
                ('laikas', models.DateField()),
                ('stadija', models.CharField(choices=[('patvirtintas', 'Patvirtintas'), ('atšauktas', 'Atšauktas'), ('grąžintas', 'Grąžintas'), ('laukiama', 'Laukiama')], max_length=12)),
                ('fk_Krepselis', models.OneToOneField(db_column='fk_Krepselis', on_delete=django.db.models.deletion.CASCADE, to='knygynas.krepselis')),
            ],
            options={
                'db_table': 'saskaitos',
            },
        ),
        migrations.CreateModel(
            name='UzsakymoKnygos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fk_Knyga', models.ForeignKey(db_column='fk_Knyga', on_delete=django.db.models.deletion.CASCADE, to='knygynas.knyga')),
                ('fk_Prekiu_uzsakymas', models.ForeignKey(db_column='fk_Prekiu_uzsakymas', on_delete=django.db.models.deletion.CASCADE, to='knygynas.prekiuuzsakymas')),
            ],
            options={
                'db_table': 'uzsakymo_knygos',
            },
        ),
        migrations.CreateModel(
            name='Vartotojas',
            fields=[
                ('id_Vartotojas', models.AutoField(primary_key=True, serialize=False)),
                ('vardas', models.CharField(max_length=255)),
                ('pavarde', models.CharField(max_length=255)),
                ('gimimo_data', models.CharField(max_length=255)),
                ('miestas', models.CharField(max_length=255)),
                ('el_pastas', models.CharField(max_length=255)),
                ('pasto_kodas', models.CharField(max_length=255)),
                ('adresas', models.CharField(max_length=255)),
                ('slaptazodis', models.CharField(max_length=255)),
                ('slapyvardis', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('registruotas', 'Registruotas'), ('neregistruotas', 'Neregistruotas')], max_length=14)),
            ],
            options={
                'db_table': 'vartotojai',
            },
        ),
        migrations.DeleteModel(
            name='TodoItem',
        ),
        migrations.AddField(
            model_name='sandelioknygos',
            name='fk_Sandelis',
            field=models.ForeignKey(db_column='fk_Sandelis', on_delete=django.db.models.deletion.CASCADE, to='knygynas.sandelis'),
        ),
        migrations.AddField(
            model_name='kurjerio_knygos',
            name='fk_Kurjeris',
            field=models.ForeignKey(db_column='fk_Kurjeris', on_delete=django.db.models.deletion.CASCADE, to='knygynas.kurjeris'),
        ),
        migrations.AddField(
            model_name='kurjerio_knygos',
            name='fk_Sandelis',
            field=models.ForeignKey(db_column='fk_Sandelis', on_delete=django.db.models.deletion.CASCADE, to='knygynas.sandelis'),
        ),
        migrations.AddField(
            model_name='krepselis',
            name='fk_Kurjeris',
            field=models.ForeignKey(db_column='fk_Kurjeris', on_delete=django.db.models.deletion.CASCADE, to='knygynas.kurjeris'),
        ),
        migrations.AddField(
            model_name='krepselis',
            name='fk_Vartotojas',
            field=models.ForeignKey(db_column='fk_Vartotojas', on_delete=django.db.models.deletion.CASCADE, to='knygynas.vartotojas'),
        ),
        migrations.AddField(
            model_name='krepselioknyga',
            name='fk_Krepselis',
            field=models.ForeignKey(db_column='fk_Krepselis', on_delete=django.db.models.deletion.CASCADE, to='knygynas.krepselis'),
        ),
        migrations.AddField(
            model_name='knyga',
            name='fk_Leidykla',
            field=models.ForeignKey(db_column='fk_Leidykla', on_delete=django.db.models.deletion.CASCADE, to='knygynas.leidykla'),
        ),
        migrations.AddConstraint(
            model_name='uzsakymoknygos',
            constraint=models.UniqueConstraint(fields=('fk_Knyga', 'fk_Prekiu_uzsakymas'), name='unique_knyga_uzsakymas'),
        ),
        migrations.AddConstraint(
            model_name='sandelioknygos',
            constraint=models.UniqueConstraint(fields=('fk_Sandelis', 'fk_Knyga'), name='unique_sandelis_knyga'),
        ),
        migrations.AddConstraint(
            model_name='kurjerio_knygos',
            constraint=models.UniqueConstraint(fields=('fk_Kurjeris', 'fk_Sandelis'), name='unique_kurjeris_sandelis'),
        ),
        migrations.AddConstraint(
            model_name='krepselioknyga',
            constraint=models.UniqueConstraint(fields=('fk_Krepselis', 'fk_Knyga'), name='unique_krepselis_knyga'),
        ),
    ]
