from django.contrib import admin
from .models import User, Diary, Todo

# Register your models here.
admin.site.register(User)
admin.site.register(Diary)
admin.site.register(Todo)