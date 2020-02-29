
from django.shortcuts import render
from rest_framework import generics


from ratings.models import Show, Ratings, Recommendations
from api.serializers import ShowSerializer, RatingsSerializer, RecommendationsSerializer


# Create your views here.


class ApiShows(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class ApiRatings(generics.ListCreateAPIView):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer


class ApiRecommendations(generics.ListCreateAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer

