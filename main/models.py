from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")


class ProductAccess(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="accesses"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accesses")

    class Meta:
        unique_together = ("product", "user")


class Lesson(models.Model):
    products = models.ManyToManyField(Product, related_name="lessons")
    name = models.CharField(max_length=360)
    url = models.URLField()
    duration = models.PositiveIntegerField()


class LessonViewing(models.Model):
    class ViewingStatus(models.TextChoices):
        VIEWED = "Y", _("Просмотрено")
        NOTVIEWED = "N", _("Не просмотрено")

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="viewings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewings")
    duration = models.PositiveIntegerField()
    status = models.CharField(
        max_length=2, choices=ViewingStatus.choices, default=ViewingStatus.NOTVIEWED
    )
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("lesson", "user")
