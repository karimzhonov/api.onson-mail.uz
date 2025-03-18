from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Country
from .serializers import CompanySerializer, CountrySerializer


class CompanyView(ListAPIView):
    pagination_class = None
    serializer_class =  CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.companies.all()


class CountryView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(company__sub=self.kwargs.get('slug'))
    