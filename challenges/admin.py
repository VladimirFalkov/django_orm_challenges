from django.contrib import admin
from .models import Laptop
from .models import Category
from .models import Post

admin.site.register(Laptop)
admin.site.register(Category)
admin.site.register(Post)
