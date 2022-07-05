from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Review, Movie
from movie_app.serializers import DirectorSerializer, ReviewSerializer, MovieSerializer, \
    DirectorDetailSerializer, MovieDetailSerializer, ReviewDetailSerializer, DirectorValidateSerializer, \
    MovieValidateSerializer, ReviewValidateSerializer, UserLoginSerializer, UserCreateSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data, )
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        director = Director.objects.create(**serializer.director_data)
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'директор создан'})


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        review = Review.objects.create(**serializer.review_data)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'отзыв создан'})


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        film = Movie.objects.create(**serializer.movie_data)
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'создан фильм'})


@api_view(['GET', 'DELETE', 'PUT'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorDetailSerializer(director).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director.delete()
    elif request.method == 'PUT':
        title = request.data.get('title', '')
        director.title = title
        director.save()
        return Response(data=DirectorDetailSerializer(Director).data)


@api_view(['GET', 'DELETE', 'PUT'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieDetailSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        movie = request.data.get('movie', '')
        title = request.data.get('title', '')
        director = request.data.get('director', '')
        movie.title = title
        movie.director = director
        movie.save()
        return Response(data=MovieDetailSerializer(Movie).data)


@api_view(['GET', 'DELETE', 'PUT'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, )
    elif request.method == 'PUT':
        text = request.data.get('text', '')
        movie = request.data.get('movie', '')
        stars = request.data.get('stars', '')
        review.text = text
        review.movie = movie
        review.stars = stars
        review.save()
        return Response(data=ReviewDetailSerializer(Review).data)


@api_view(['POST'])
def authorization_view(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_403_FORBIDDEN,
                    data={'error': 'credential data are wrong'})


@api_view(['POST'])
def registration_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
