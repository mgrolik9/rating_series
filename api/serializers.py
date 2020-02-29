
from rest_framework import serializers


from django.contrib.auth.models import User


from ratings.models import Show, Ratings, Recommendations


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'title', 'year', 'platform')


class RatingsSerializer(serializers.ModelSerializer):
    show = serializers.SlugRelatedField(slug_field='title', queryset=Show.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Ratings
        fields = ('id', 'show', 'user', 'rating', 'added_date')


class RecommendationsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    shows = serializers.SlugRelatedField(many=True, slug_field='title', queryset=Show.objects.all())

    class Meta:
        model = Recommendations
        fields = ('id', 'user', 'shows')