from django.db import models
from django.db.models import OuterRef, Subquery, Count, Q, Sum
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import HasProductAccess
from .serializers import (
    LessonSerializer,
    LessonWithDateSerializer,
    ProductsStatisticsSerializer,
)
from .models import LessonViewing, Lesson, ProductAccess, Product

User = get_user_model()


class SubqueryCount(Subquery):
    users = User.objects.filter(is_staff=False).count()
    template = f"(SELECT count(*) FROM (%(subquery)s)) * 1.0 / {users} * 100"
    output_field = models.FloatField()


class UserLessonsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        viewing = LessonViewing.objects.filter(
            lesson=OuterRef("pk"), user=user
        ).order_by("-date")
        lessons = Lesson.objects.filter(products__accesses__user=user).annotate(
            viewing=Subquery(viewing.values("duration")[:1]),
            status=Subquery(viewing.values("status")[:1]),
        )
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonsOfConcreteProductAPIView(APIView):
    permission_classes = [IsAuthenticated, HasProductAccess]

    def get(self, request, **kwargs):
        user = request.user
        id = kwargs.get("id")
        viewing = LessonViewing.objects.filter(
            lesson=OuterRef("pk"), user=user
        ).order_by("-date")
        lessons = Lesson.objects.filter(products__id=id).annotate(
            viewing=Subquery(viewing.values("duration")[:1]),
            status=Subquery(viewing.values("status")[:1]),
            date=Subquery(viewing.values("date")[:1]),
        )
        serializer = LessonWithDateSerializer(lessons, many=True)
        return Response(serializer.data)


class ProductsStatisticsAPIView(APIView):
    def get(self, request):
        accesses = ProductAccess.objects.filter(product__id=OuterRef("pk"))
        products = Product.objects.all().annotate(
            lesson_views=Count(
                "lessons__viewings",
                filter=Q(lessons__viewings__status=LessonViewing.ViewingStatus.VIEWED),
            ),
            viewing_duration=Sum("lessons__viewings__duration"),
            students_studying=Count(
                "lessons__viewings",
                filter=Q(
                    lessons__viewings__status=LessonViewing.ViewingStatus.NOTVIEWED
                ),
            ),
            selling_percentage=SubqueryCount(accesses),
        )
        serializer = ProductsStatisticsSerializer(products, many=True)
        return Response(serializer.data)
