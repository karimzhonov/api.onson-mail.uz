import django_filters.rest_framework as filters

from django_celery_results.models import TaskResult


class TaskResultFilter(filters.FilterSet):
    subscriberSystem = filters.CharFilter(method='subscriberSystemFilter')
    date = filters.DateFilter(method='dateFilter')

    class Meta:
        model = TaskResult
        fields = ['subscriberSystem', 'date']

    def subscriberSystemFilter(self, queryset, name, value):
        return queryset.filter(task_kwargs__systems__contains=value)

    def dateFilter(self, queryset, name, value):
        return queryset.filter(date_started__date=value)