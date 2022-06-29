from abc import ABC

from rest_framework import serializers
from movie_app.models import Director, Review, Movie
from rest_framework.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'title'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text Movie'.split()


def get_custom_reviews(movie):
    data = movie.reviews.all()
    return ReviewSerializer(data, many=True).data


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()

    class Meta:
        model = Movie
        fields = 'rating title description duration director review'.split()


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3, max_length=100)
    movie = serializers.CharField(required=False)
    stars = serializers.IntegerField(required=False, allow_null=True,
                                     default=None)

    @property
    def review_data(self):
        dict_ = {
            'text': self.validated_data.get('text', ''),
            'movie': self.validated_data.get('movie', ''),
            'stars': self.validated_data.get('stars', ''),
        }
        return dict_

    def validate_movie(self, movie):
        try:
            Movie.objects.get(id=movie)
        except:
            raise ValidationError('Movie not found')

class DirectorValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)

    @property
    def director_data(self):
        dict_ = {
            'title': self.validated_data.get('title', '')
        }
        return dict_

class MovieValidateSerializer(serializers.Serializer):
    review = serializers.CharField(min_length=3, max_length=100)
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.FloatField(max_value=0.5, min_value=100000)
    duration = serializers.CharField(min_length=3, max_length=100)
    director = serializers.CharField(child=serializers.IntegerField)

    @property
    def movie_data(self):
        dict_ = {
            'movie': self.data.get('movie', ''),
            'title': self.data.get('title', ''),
            'director': self.data.get('director', ''),
        }
        return dict_