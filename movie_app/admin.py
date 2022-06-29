from django.contrib import admin
from movie_app.models import Director, Review, Movie

# Register your models here.

admin.site.register(Director)
admin.site.register(Review)
admin.site.register(Movie)
