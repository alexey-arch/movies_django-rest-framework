from rest_framework import serializers
from .models import Movie, Review, Rating, Actor

class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializater(serializers.ModelSerializer):
    """Получение актеров"""
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')
        

class ActorDetailSerializater(serializers.ModelSerializer):
    """Получение полной информации актеров"""
    class Meta:
        model = Actor
        fields = '__all__'


class CreateRatingSerializer(serializers.ModelSerializer):
    """Создание обновление рейтинга"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def crate(self, validated_data):
        rating, _ = Rating.objects.update_to_create(
            ip=validated_data.get('ip',None),
            movie=validated_data.get('movie',None),
            default=validated_data.get('star'))

        return rating


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user','middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Создание отзыва"""
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыво"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Информация фильма"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializater(read_only=True, many=True)
    actors = ActorListSerializater(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft',)