from rest_framework import serializers
from .models import Lesson, Product


class LessonSerializer(serializers.ModelSerializer):
    viewing = serializers.IntegerField()
    status = serializers.CharField()

    class Meta:
        model = Lesson
        fields = ["name", "url", "duration", "viewing", "status"]


class LessonWithDateSerializer(LessonSerializer):
    date = serializers.DateField()

    class Meta:
        model = Lesson
        fields = ["name", "url", "duration", "viewing", "status", "date"]


class ProductsStatisticsSerializer(serializers.ModelSerializer):
    lesson_views = serializers.IntegerField()
    viewing_duration = serializers.IntegerField()
    students_studying = serializers.IntegerField()
    selling_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            "id",
            "lesson_views",
            "viewing_duration",
            "students_studying",
            "selling_percentage",
        ]
