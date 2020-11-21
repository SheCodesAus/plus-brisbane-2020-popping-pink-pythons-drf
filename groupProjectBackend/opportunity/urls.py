from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('opportunity/', views.OpportunityList.as_view()),
    path('opportunity/<int:pk>/', views.OpportunityDetail.as_view()),
    path('/favourites/', views.OpportunityLatest.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)