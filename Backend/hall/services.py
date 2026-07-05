from typing import List
from django.db import transaction

from .models import Hall, Seat


def get_row_char_by_number(number: int) -> str:
    result = ""

    while number > 0:
        number -= 1
        result = chr(ord('A') + number % 26) + result
        number //= 26

    return result



def create_hall(name: str, rows: int, seats_per_row: int, blocks: int) -> Hall:
    with transaction.atomic():
        if Hall.objects.filter(name=name).exists():
            raise ValueError("Hall with this name already exists")

        hall = Hall.objects.create(name=name, rows=rows, seats_per_row=seats_per_row, blocks=blocks)
        seats = [
            Seat(hall=hall, row_num=row, seat_number=seat, block_num=block)
            for block in range(1, blocks + 1)
            for row in range(1, rows + 1)
            for seat in range(1, seats_per_row + 1)
        ]
        Seat.objects.bulk_create(seats)
        return hall


def change_seats_status(seat_ids: List[int], is_available: bool) -> Seat:
    seats = Seat.objects.filter(id__in=seat_ids, )
    seats.update(is_available=is_available)
    return seats
