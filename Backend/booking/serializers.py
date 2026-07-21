from django.db import transaction
from django.utils.ipv6 import ValidationError
from rest_framework import serializers

from Backend.hall.models import Seat

from ..hall.serializers import HallShortSerializer, HallSerializer, SeatSerializer
from ..catalog.serializers import MovieShortSerializer
from .models import Session, Ticket
from .services import book_tickets, create_session



class SessionReadSerializer(serializers.ModelSerializer):
    movie = MovieShortSerializer()
    hall = HallShortSerializer()
    class Meta:
        model = Session
        fields = ['id','movie', 'hall', 'starts_at', 'price', 'status']

class SessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['movie_id', 'hall_id', 'starts_at', 'price', 'status']

    def create(self, validated_data):
        return create_session(**validated_data)

    def update(self, instance, validated_data):
        new_hall = validated_data.get("hall")
        new_movie = validated_data.get("movie")

        has_tickets = instance.tickets.exists()

        if has_tickets and ("hall" in validated_data or "movie" in validated_data):
            raise serializers.ValidationError(
                "Cannot change hall or movie for session with tickets"
            )

        if instance.status != "UNPUBLISHED" and ("hall" in validated_data or "movie" in validated_data):
            raise serializers.ValidationError(
                "Cannot change hall or movie for published session"
        )

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class SessionDetailSerializer(serializers.ModelSerializer):
    movie = MovieShortSerializer()
    hall = HallSerializer()
    booked_seat_ids = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'movie', 'hall', 'starts_at', 'price', 'status', 'booked_seat_ids']

    def get_booked_seat_ids(self, obj):
        return list(obj.tickets.values_list('seat_id', flat=True))

class TicketReadSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()
    session = SessionReadSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'session', 'seat', 'price', 'status', 'created_at']


class TicketWriteSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=True)
    seat_ids = serializers.ListField(child=serializers.IntegerField(),required=True)

    def validate_session_id(self, value):
        if not Session.objects.filter(id=value).exists():
            raise ValidationError("Session doesnt exists")
        return value

    def validate(self, attrs):
        seat_ids = attrs["seat_ids"]
        session_id = attrs["session_id"]

        session = Session.objects.filter(id=session_id).first()
        if session is None:
            raise serializers.ValidationError({
                "session_id": "Session doesn't exist"
            })


        for seat_id in seat_ids:
            seat = Seat.objects.get(id=seat_id)
            if seat is None:
                raise serializers.ValidationError({
                    "seat_id": "Seat doesn't exist"
                })

            if seat.hall_id != session.hall_id:
                raise serializers.ValidationError({
                    "seat_id": "Seat doesn't belong to the session hall"
                })

        return attrs



    def create(self, validated_data):
        request = self.context['request']
        tickets = book_tickets(
            session_id=validated_data['session_id'],
            seat_ids=validated_data['seat_ids'],
            user_id=request.user.id,
        )
        return tickets

    def update(self, instance, validated_data):
        pass