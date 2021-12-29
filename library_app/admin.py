from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(IssuedBook)
admin.site.register(IssuedBook1)