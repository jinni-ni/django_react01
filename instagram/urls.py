from django.urls import path, register_converter
from . import views

class YearConverter:
    regex = r"20\d{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)

register_converter(YearConverter, 'year')

urlpatterns =[
    path('', views.post_list),
    path('<int:pk>/', views.post_detail),
    path('archives/<year:year>/', views.archives_year)
]
