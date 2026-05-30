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
                return Response({"error": str(e)},status = status.HTTP_400_BAD_REQUEST)


class CreateActorView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ActorSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                franchise = create_actor(**serializer.validated_data)
                response_data = self.serializer_class(franchise).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)},status = status.HTTP_400_BAD_REQUEST)

class CreateGenreView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GenreSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                franchise = create_genre(**serializer.validated_data)
                response_data = self.serializer_class(franchise).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)},status = status.HTTP_400_BAD_REQUEST)

class BookMovieView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        seats = request.data.get('seats', []) 
        
        
        MovieBooking.objects.create(
            user=request.user, 
            movie=movie, 
            seats=seats
        )
        return Response({"message": "Tickets bought successfully"}, status=status.HTTP_201_CREATED)


class MovieBookedSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        get_object_or_404(Movie, id=movie_id)
        booked: list[str] = []
        for booking in MovieBooking.objects.filter(movie_id=movie_id).only('seats'):
            raw = booking.seats or []
            if isinstance(raw, list):
                for seat in raw:
                    if isinstance(seat, str) and seat not in booked:
                        booked.append(seat)
        return Response({"booked_seats": booked},status=status.HTTP_201_CREATED)



class MyTicketsView(APIView):
    def get(self, request):
        bookings = MovieBooking.objects.filter(user=request.user).select_related('movie')
        
        serializer = MovieBookingSerializer(bookings, many=True,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)