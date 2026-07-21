import datetime

from django.db import IntegrityError, transaction

from .models import Session, Ticket
from ..hall.models import Seat, Hall
from ..catalog.models import Movie


def create_session(hall_id: int , starts_at: datetime,price: int, status: str = None, movie_id: int = None,) -> Session:

    with transaction.atomic():
        try:
            hall = Hall.objects.get(id=hall_id)
        
        except Hall.DoesNotExist:
            raise ValueError("Hall does not exist")
        if status is None or movie_id is None:
            status = "UNPUBLISHED"
            session = Session.objects.create(hall=hall, starts_at=starts_at, price = price,status = status)
        else:
            movie = Movie.objects.get(id = movie_id)
            session = Session.objects.create(movie=movie, hall=hall, starts_at=starts_at, price = price,status = status)
        
        return session

def book_tickets(session_id: int, seat_ids:  list[int], user_id: int, price:int = None ) -> list[Ticket]:
    with transaction.atomic():
        session = Session.objects.select_related('hall').get(id=session_id)
        if session.status != "PUBLISHED":
                raise ValueError("Cannot book seats in unpublished session")

        tickets = []
        for seat_id in sorted(set(seat_ids)):
            seat = Seat.objects.select_for_update().get(id=seat_id)
            if seat.hall_id != session.hall_id:
                raise ValueError(f"Seat with id {seat_id} doesnt exists in this hall")

            if not seat.is_available:
                raise ValueError("Seat isnt available")

            if Ticket.objects.filter(session = session, seat = seat).exists():
                raise ValueError(f"Seat in row {seat.row_num}, block {seat.block_num}, seat {seat.seat_number} has already been booked")

            try:
                updated_seat = Seat.objects.select_for_update().filter(id=seat_id, session=session)
                ticket = Ticket.objects.create(session=session, seat=updated_seat, user_id=user_id, price = price if price is not None else session.price )
                tickets.append(ticket)
            except IntegrityError:
                raise ValueError(
                    f"Seat in row {seat.row_num}, block {seat.block_num}, seat {seat.seat_number} has already been booked")

        return tickets

def update_tickets(session_id: int, seat_ids:  list[int]):
    pass