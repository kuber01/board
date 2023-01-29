from django_filters import FilterSet
from .models import Response


class PostFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'post__title': ['icontains'],
        }
