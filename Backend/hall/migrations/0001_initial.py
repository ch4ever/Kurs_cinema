from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('rows', models.PositiveSmallIntegerField()),
                ('seats_per_row', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_num', models.PositiveSmallIntegerField()),
                ('seat_number', models.PositiveSmallIntegerField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='hall.hall')),
            ],
        ),
        migrations.AddConstraint(
            model_name='seat',
            constraint=models.UniqueConstraint(fields=('hall', 'row_num', 'seat_number'), name='unique_seat'),
        ),
    ]
