from django.urls import path
from .views import (
    UserLessonsAPIView,
    LessonsOfConcreteProductAPIView,
    ProductsStatisticsAPIView,
)

urlpatterns = [
    path("lessons/", UserLessonsAPIView.as_view(), name="all-lessons"),
    path(
        "products/<int:id>/lessons/",
        LessonsOfConcreteProductAPIView.as_view(),
        name="product-lessons",
    ),
    path(
        "products/statistics/",
        ProductsStatisticsAPIView.as_view(),
        name="products-statistics",
    ),
]
