from django.db import models
from Backend.Kursach import settings

class Session(models.Model):
    movie = models.ForeignKey(
        'catalog.Movie',
        on_delete=models.CASCADE,
        related_name='sessions',
        null=True, blank=True
    )
    hall = models.ForeignKey(
        'hall.Hall',
        on_delete=models.PROTECT,
        related_name='sessions',
    )
    starts_at = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(choices=(("PUBLISHED","Published"),("UNPUBLISHED","Unpublished")))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hall', 'starts_at'],
                name='unique_hall_session_time',
            )
        ]



class Ticket(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    seat = models.ForeignKey(
        'hall.Seat',
        on_delete=models.PROTECT,
        related_name='tickets',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    #TODO tasks for status changes
    status = models.CharField(choices=(('AVAILABLE', 'Available'),('EXPIRED', 'Expired'),('USED','Used')), default="AVAILABLE")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'seat'],
                name='unique_ticket_session_seat',
            )
        ]