from django.db import models


# Create your models here.

class Director(models.Model):
    title = models.CharField(max_length=100)


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    movie = models.CharField(max_length=100)
    stars = models.IntegerField(default=-1)


class Movie(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    @property
    def rating(self):
        review = self.review.all()
        if not review:
            return 0
        average = 0
        for i in review:
            average += i.stars
        return average / review.count()


STAR_CHOICES = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)
