
from django.urls import path


from api.views import ApiShows, ApiRatings, ApiRecommendations


urlpatterns = [
    path('api/shows/', ApiShows.as_view(), name="api-shows"),
    path('api/ratings', ApiRatings.as_view(), name="api-ratings"),
    path('api/recommendations', ApiRecommendations.as_view(), name="api-recommendations")
]
