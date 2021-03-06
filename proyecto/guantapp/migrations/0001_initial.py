# Generated by Django 2.2 on 2019-12-04 16:47

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Usuario inválido', regex='[A-Za-z0-9]{5,50}')])),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Nombre inválido', regex='[A-Za-z]{2,50}')])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Apellido inválido', regex='[A-Za-z]{2,50}')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Nombre de categoría inválido', regex='[A-Za-z\\s]{4,50}')])),
                ('descripcion', models.TextField(default='descripción de la categoría')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='guantapp.Categoria')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Nombre de marca inválido', regex='[A-Za-z0-9\\s]{4,50}')])),
                ('slogan', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Eslogan inválido', regex='[A-Za-z0-9\\s]{4,50}')])),
                ('descripcion', models.TextField(default='descripción marca', max_length=200)),
                ('marca_picture', models.ImageField(upload_to='')),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('num_orden', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now=True)),
                ('hora', models.TimeField(auto_now=True)),
                ('estado', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(upload_to='')),
                ('phone', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Teléfono inválido', regex='[267][0-9]{7}')])),
                ('country', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='País inválido', regex='[A-Za-z\\s]{4,50}')])),
                ('city', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Ciudad inválida', regex='[A-Za-z\\s]{3,50}')])),
                ('nit', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='NIT inválido', regex='[0-9]{14}')])),
                ('nrc', models.CharField(max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Nombre de producto inválido', regex='[A-Za-z0-9\\s]{4,50}')])),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.TextField(default='descripción del producto')),
                ('producto_picture', models.ImageField(upload_to='')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoria', to='guantapp.Categoria')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marca', to='guantapp.Marca')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateField(auto_now=True)),
                ('metodo_pago', models.IntegerField()),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='guantapp.Orden')),
            ],
        ),
        migrations.AddField(
            model_name='orden',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comprador', to='guantapp.UserProfile'),
        ),
        migrations.AddField(
            model_name='orden',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor', to='guantapp.UserProfile'),
        ),
        migrations.AddField(
            model_name='marca',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile_Marca', to='guantapp.UserProfile'),
        ),
        migrations.CreateModel(
            name='ListaDeseos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='guantapp.Producto')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile_lista_deseos', to='guantapp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='LineaOrden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guantapp.Orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guantapp.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor_calificacion', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(message='Valor ingresado inválido', regex='[1-5]')])),
                ('descripcion', models.TextField(default='descripción de la calificación')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guantapp.Producto')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guantapp.UserProfile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='calificacion',
            constraint=models.UniqueConstraint(fields=('producto', 'user_profile'), name='unique_calificacion'),
        ),
    ]
