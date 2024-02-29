from django.contrib import admin
from .models import Product, ProductAccess, Lesson, LessonViewing

admin.site.register(Product)
admin.site.register(ProductAccess)
admin.site.register(Lesson)
admin.site.register(LessonViewing)
# Register your models here.
