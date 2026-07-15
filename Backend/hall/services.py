from typing import List
from django.db import transaction
from django.db.models import Q

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

def create_seat(
    hall_id: int,
    block_num: int,
    row_num:int, 
    seat_num: int, is_available:bool = True) -> Seat:
    seat = Seat.objects.create(hall_id=hall_id, block_num=block_num ,row_num=row_num, seat_num =seat_num, is_available= is_available)
    return seat

def delete_seat(hall_id:int, block_num:int, row_num:int, seat_num: int):
    Seat.objects.delete(hall_id=hall_id, block_num=block_num ,row_num=row_num, seat_num =seat_num)
    
# TODO implement booking logic -> cancel or seans seat is_available = False
def update_hall(
    hall: Hall,
    name: str | None = None,
    blocks: int | None = None,
    rows: int | None = None,
    seats_per_row: int | None = None,
) -> Hall:
    new_blocks = blocks if blocks is not None else hall.blocks
    new_rows = rows if rows is not None else hall.rows
    new_seats_per_row = seats_per_row if seats_per_row is not None else hall.seats_per_row

    with transaction.atomic():
        if name is not None:
            hall.name = name

        hall.blocks = new_blocks
        hall.rows = new_rows
        hall.seats_per_row = new_seats_per_row
        hall.save()

        Seat.objects.filter(hall=hall).filter(
            Q(block_num__gt=new_blocks) |
            Q(row_num__gt=new_rows) |
            Q(seat_number__gt=new_seats_per_row)
        ).delete()

        existing = set(
            Seat.objects.filter(hall=hall).values_list(
                'block_num',
                'row_num',
                'seat_number',
            )
        )

        seats_to_create = []
        for block in range(1, new_blocks + 1):
            for row in range(1, new_rows + 1):
                for seat in range(1, new_seats_per_row + 1):
                    key = (block, row, seat)
                    if key not in existing:
                        seats_to_create.append(
                            Seat(
                                hall=hall,
                                block_num=block,
                                row_num=row,
                                seat_number=seat,
                            )
                        )

        Seat.objects.bulk_create(seats_to_create)

    return hall

def change_seats_status(seat_ids: List[int], is_available: bool) -> Seat:
    seats = Seat.objects.filter(id__in=seat_ids, )
    seats.update(is_available=is_available)
    return seats
