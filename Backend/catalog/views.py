from django.db.models.base import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import create_genre, create_actor, create_franchise
from .serializers import ActorSerializer, GenreSerializer, MovieCreateSerializer, MovieSerializer, FranchiseSerializer,MovieBookingSerializer
from .models import Movie, MovieBooking
from siteuser.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MovieViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MovieCreateSerializer
        return MovieSerializer
        

    def get_queryset(self):
        movie = super().get_queryset()

        if self.action in ['list','retrieve']:
            movie = movie.select_related('franchise').prefetch_related('actors','genres')
        return movie

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return super().get_permissions()


class CreateFranchiseView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FranchiseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                franchise = create_franchise(**serializer.validated_data)
                response_data = self.serializer_class(franchise).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)},status = status.HTTP_400_BAD_REQUEST)


class CreateActorView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ActorSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                actor = create_actor(**serializer.validated_data)
                response_data = self.serializer_class(actor).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)},status = status.HTTP_400_BAD_REQUEST)

class CreateGenreView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GenreSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                genre = create_genre(**serializer.validated_data)
                response_data = self.serializer_class(genre).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)},status = status.HTTP_400_BAD_REQUEST)

class BookMovieView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        requested_seats = request.data.get('seats', []) 
        
        if not requested_seats:
            return Response({"detail": "Empty seats list"}, status=status.HTTP_400_BAD_REQUEST)

        
        with transaction.atomic():
            booked_seats_qs = MovieBooking.objects.filter(movie=movie).values_list('seats', flat=True)
            already_booked = set()
            for seats_list in booked_seats_qs:
                if seats_list:
                    already_booked.update(seats_list)

            
            overlap = set(requested_seats).intersection(already_booked)
            if overlap:
                return Response(
                    {"detail": f"Seats {', '.join(overlap)} already booked!"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            MovieBooking.objects.create(
                user=request.user, 
                movie=movie, 
                seats=requested_seats
            )
            
        return Response({"detail": "Tickets bought successfully"}, status=status.HTTP_201_CREATED)


class MovieBookedSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        get_object_or_404(Movie, id=movie_id)
        booked = set()
        for booking in MovieBooking.objects.filter(movie_id=movie_id).only('seats'):
            if booking.seats:
                booked.update(booking.seats)
                
        return Response({"booked_seats": list(booked)}, status=status.HTTP_200_OK)


class MyTicketsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        bookings = MovieBooking.objects.filter(user=request.user).select_related('movie')
        
        serializer = MovieBookingSerializer(bookings, many=True,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)