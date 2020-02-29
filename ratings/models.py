
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PLATFORM = (
    (1, 'Netflix'),
    (2, 'HBO'),
    (3, 'Inne')
)

RATINGS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)


class Show(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tytuł serialu')
    year = models.CharField(max_length=10, verbose_name='Rok wydania')
    platform = models.IntegerField(choices=PLATFORM, default=3, verbose_name='Gdzie znajde')

    def __str__(self):
        return self.title


class Ratings(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, verbose_name='Ocena')
    comment = models.CharField(max_length=100, blank=True, verbose_name='Komentarz do oceny')
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.show.title


class Recommendations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shows = models.ManyToManyField(Show, related_name='recommendations_set')

    def __str__(self):
        return self.user.username


