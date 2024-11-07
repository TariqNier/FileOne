from .models import *
import django_filters

class CoursessFilter(django_filters.FilterSet):

    

    class Meta:
        model = Course
        fields = '__all__'