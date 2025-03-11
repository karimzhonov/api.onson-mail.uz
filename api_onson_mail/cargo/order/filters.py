from django_filters import rest_framework as filters
from cargo.order.models import Order, Part


class OrderFilter(filters.FilterSet):
    status_sql = filters.BaseInFilter(method='filter_status_')

    class Meta:
        model = Order
        fields = ['parts', 'status_sql']

    def filter_status_(self, queryset, name, value):
        queryset = queryset.annotate(
            status_sql=Order.status_sql()
        )
        return queryset.filter(status_sql__in=value)


class PartFilter(filters.FilterSet):
    ended = filters.BooleanFilter(method='filter_ended')

    class Meta:
        model = Part
        fields = ['country', 'status', 'ended']

    def filter_ended(self, queryset, name, value):
        statuses = ["process_received_datetime"] if value \
            else ["create_time", "departure_datetime",
                  "enter_uzb_datetime", "process_customs_datetime",
                  "process_local_datetime"]
        return queryset.filter(status__in=statuses)
