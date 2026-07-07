from django.db.models.base import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ActorSerializer, GenreSerializer, MovieCreateSerializer, MovieSerializer, FranchiseSerializer,MovieBookingSerializer
from .models import Actor, Franchise, Genre, Movie, MovieBooking
from siteuser.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MovieViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication,]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ('create','partial_update','update'):
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



@extend_schema_view(
    list = extend_schema(
        summary="Franchise list",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Franchise retrieve",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer()},
    ),
    create = extend_schema(
        summary="Franchise create",
        tags=["Franchise"],
        responses={
            status.HTTP_201_CREATED: FranchiseSerializer}
    ),
    destroy = extend_schema(
        summary="Franchise delete",
        tags=["Franchise"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Franchise patch",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK:FranchiseSerializer() }
    ),
    update = extend_schema(
        summary="Franchise update",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer() }
    ),
)
class FranchiseViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = FranchiseSerializer
    queryset = Franchise.objects.all()

    #TODO do i need this?
    def get_queryset(self):
        query = super().get_queryset()
        if self.action in ['retrieve','list']:
            return query.prefetch_related('movies')
        return query 

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()


@extend_schema_view(
    list = extend_schema(
        summary="Actors list",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Actor retrieve",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer()},
    ),
    create = extend_schema(
        summary="Actor create",
        tags=["Actor"],
        responses={
            status.HTTP_201_CREATED: ActorSerializer}
    ),
    destroy = extend_schema(
        summary="Actors delete",
        tags=["Actor"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Actor patch",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK:ActorSerializer() }
    ),
    update = extend_schema(
        summary="Actor update",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer() }
    ),
)
class ActorViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()

   
@extend_schema_view(
    list = extend_schema(
        summary="Genres list",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Genre retrieve",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer()},
    ),
    create = extend_schema(
        summary="Genres create",
        tags=["Genre"],
        responses={
            status.HTTP_201_CREATED: GenreSerializer}
    ),
    destroy = extend_schema(
        summary="Genres delete",
        tags=["Genre"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Genres patch",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK:GenreSerializer() }
    ),
    update = extend_schema(
        summary="Genre update",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer() }
    ),
)
class GenreViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()



#TODO make personal app for this
class BookMovieView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
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

    def get(self, request):
        movie_id = request.data['movie_id']
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