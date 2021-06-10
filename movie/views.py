from django.shortcuts import render
from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (
    MovieListSerializer, 
    MovieDetailSerializer, 
    ReviewCreateSerializer, 
    CreateRatingSerializer, 
    ActorListSerializater,
    ActorDetailSerializater,
    )
from .service import get_client_ip, MovieFilter, PaginationMovie

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление списка фильмов"""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovie

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", 
                                    filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )

        return movies

    def get_serializer_class(self):
        if self.action =='list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Представление создание отзыва"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Представление создание рейтинга"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Предстовление списка актеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializater
        elif self.action == 'retrieve':
            return ActorDetailSerializater



# class MovieListView(generics.ListAPIView):
#     """Представление списка фильмов"""

#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     # serializer_class = MovieListSerializer
#     # permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", 
#                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )

#         return movies
        

# class MovieDetailView(generics.RetrieveAPIView):
#     """Представление списка фильмов"""

#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer


# class ReviewCreateView(generics.CreateAPIView):
#     """Представление создание отзыва"""

#     serializer_class = ReviewCreateSerializer


# class AddStarRatingView(generics.CreateAPIView):
#     """Представление создание рейтинга"""

#     serializer_class = CreateRatingSerializer
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))



# class ActorListView(generics.ListAPIView):
#     """Предстовление списка актеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializater


# class ActorDetailView(generics.RetrieveAPIView):
#     """Предстовление списка актеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializater