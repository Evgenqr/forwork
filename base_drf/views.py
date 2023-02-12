from rest_framework import generics
from base.models import Document
from .serializers import DocumentSerializer, DocumentDetailSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from .permissions import IsAdminOrReadOnly


class DocumentAPIList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class DocumentAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAdminOrReadOnly, )


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )
