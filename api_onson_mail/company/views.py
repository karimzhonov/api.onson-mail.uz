from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CompanySerializer


class CompanyView(ListAPIView):
    pagination_class = None
    serializer_class =  CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.companies.all()
