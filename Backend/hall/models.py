from django.db import models

# Create your models here.

class Hall(models.Model):
    name = models.CharField(max_length=50, unique=True)
    blocks = models.PositiveSmallIntegerField(default=2)
    rows = models.PositiveSmallIntegerField(default=10)
    seats_per_row = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row_num = models.PositiveSmallIntegerField(blank=True, null=True)
    block_num = models.PositiveSmallIntegerField(blank=True, null=True)
    seat_number = models.PositiveSmallIntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hall', 'block_num', 'row_num', 'seat_number'], name='unique_seat')
        ]

    def __str__(self):
        return f'{self.hall.name}: block {self.block_num}, row {self.row_num}, seat {self.seat_number}'
