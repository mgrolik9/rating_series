
from django.contrib import admin


from ratings.models import Show, Ratings, Recommendations

# Register your models here.


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'platform')

@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ('show', 'user', 'rating', 'comment', 'added_date')

@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'shows_list')

    def shows_list(self, obj):
        return ", ".join([str(t) for t in obj.shows.all()])
