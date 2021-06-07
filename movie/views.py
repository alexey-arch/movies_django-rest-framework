from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer
from .service import get_client_ip

class MovieListView(APIView):
    """Представление списка фильмов"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
        

class MovieDetailView(APIView):
    """Представление списка фильмов"""
    def get(self, request, pk):
        movies = Movie.objects.get(id = pk, draft=False)
        serializer = MovieDetailSerializer(movies)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Представление создание отзыва"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Представление создание рейтинга"""

    def post(self, request):
        serializer = CreateRatingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)