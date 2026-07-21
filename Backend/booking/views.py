from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import isOwnerOrAdminOfTicket
from .models import Session, Ticket
from .serializers import SessionDetailSerializer, SessionReadSerializer, SessionWriteSerializer, TicketReadSerializer, TicketWriteSerializer
from ..siteuser.permissions import IsAdminUser

# Create your views here.


class SessionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    
    
    def get_permissions(self):
        if self.action in ["create","update","destroy","partial_update"]:
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SessionDetailSerializer
        elif self.action == "list":
            return SessionReadSerializer
        elif self.action in ["update","partial_update","create"]:
            return SessionWriteSerializer
        return SessionReadSerializer

    def get_queryset(self):
        queryset = Session.objects.all()

        if self.action in ("list") :
            return queryset.select_related("movie", "hall")
        if self.action == "retrieve":
            return queryset.select_related("movie", "hall").prefetch_related("tickets", "hall__seats")

        return queryset


class TicketViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isOwnerOrAdminOfTicket(), ]

    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return TicketReadSerializer
        else:
            return TicketWriteSerializer

    def get_queryset(self):
        query = Ticket.objects.all()
        user = self.request.user
        if self.action in ["list","retrieve"]:
            return query.select_related("session","seat").filter(user=user)
        return query

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tickets = serializer.save()

        response_serializer = TicketReadSerializer(
            tickets,
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )