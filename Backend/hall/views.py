from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import change_seats_status
from siteuser.permissions import IsAdminUser
from .serializers import HallSerializer, SeatBlockSerializer, SeatSerializer
from .models import Hall



@extend_schema_view(
    list=extend_schema(
        summary="List all halls",
        description="List all halls with their seats",
        tags=["Hall"],
        responses={
            status.HTTP_200_OK: HallSerializer(many=True)
        }
    ),
    retrieve=extend_schema(
        summary="Get a hall by ID",
        description="Get a hall by ID with its seats",
        tags=["Hall"],
        responses={
            status.HTTP_200_OK: HallSerializer(),
        }
    ),
    create=extend_schema(
        summary="Create a new hall",
        description="Create a new hall with its seats",
        tags=["Hall"],
        responses={
            status.HTTP_201_CREATED: HallSerializer(),
        }
    ),
    partial_update=extend_schema(
        summary="Partial update a hall by ID",
        description="Partial update a hall by ID with its seats",
        tags=["Hall"],
        responses={
            status.HTTP_200_OK: HallSerializer(),
        }
    ),
    destroy=extend_schema(
        summary="Delete a hall by ID",
        description="Delete a hall by ID with its seats",
        tags=["Hall"],
        responses={
            status.HTTP_204_NO_CONTENT: None,
        }
    ),
)
class HallViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = HallSerializer
    queryset = Hall.objects.prefetch_related('seats')


class SeatStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    summary="Update seat status",
    description="Update seat status by seat IDs",
    tags=["Hall"],
    responses={
        status.HTTP_200_OK: SeatSerializer(many=True),
    },
    request=SeatBlockSerializer,
    )
    def patch(self, request):
        serializer = SeatBlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            seats = change_seats_status(**serializer.validated_data)
            response_data = SeatSerializer(seats,many=True).data
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
                return Response({"detail": str(e)},status = status.HTTP_400_BAD_REQUEST)
