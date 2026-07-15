from django.db import transaction
from rest_framework import serializers
from .services import create_hall, update_hall
from .models import Hall, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'block_num', 'row_num', 'seat_number', 'is_available']

class SeatBlockSerializer(serializers.Serializer):
    seat_ids = serializers.ListField(child=serializers.IntegerField(),required = True)
    is_available = serializers.BooleanField()

    def validate_seat_ids(self, value):
        existing_count = Seat.objects.filter(id__in=value).count()
        if existing_count != len(set(value)):
            raise serializers.ValidationError('One or more seats do not exist')
        return value


class HallSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Hall
        fields = ['id', 'name', 'blocks', 'rows', 'seats_per_row', 'seats']
        read_only_fields = ['id']

    def validate_rows(self, value):
        if value < 1:
            raise serializers.ValidationError('Rows count must be greater than zero')
        return value

    def validate_seats_per_row(self, value):
        if value < 1:
            raise serializers.ValidationError('Seats per row must be greater than zero')
        return value

    def validate_blocks(self, value):
        if value < 1:
            raise serializers.ValidationError('Blocks count must be greater than zero')
        return value

    def create(self, validated_data):
        hall = create_hall(**validated_data)
        return hall

    def update(self, instance, validated_data):
        return update_hall(instance, **validated_data)
                    

