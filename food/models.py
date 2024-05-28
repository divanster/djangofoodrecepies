from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation


class Item(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=200)
    item_desc = models.TextField(max_length=4000)
    item_image = models.CharField(max_length=500, default='https://media.istockphoto.com/id/1426890025/es/foto/la'
                                                          '-pizza-de-la-que-te-olvidaste-durante-una-semana-y-se-puso'
                                                          '-mohosa.jpg?s=612x612&w=0&k=20&c'
                                                          '=r0cHrYxEjoLUoSz9VQCglgXc6Win_fFu-fjDwWfoPu4=')
    views = models.PositiveIntegerField(default=0)
    ratings = GenericRelation(Rating, related_query_name='item')

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("food:detail", kwargs={"pk": self.pk})

    def increment_views(self):
        self.views += 1
        self.save()

    def get_average_rating(self):
        ratings = Rating.objects.filter(content_type__model='item', object_id=self.id)
        if ratings.exists():
            return ratings.aggregate(models.Avg('average'))['average__avg']
        return 0

    def get_rating_count(self):
        ratings = Rating.objects.filter(content_type__model='item', object_id=self.id)
        return ratings.count()

    def get_user_rating(self, user):
        user_rating = Rating.objects.filter(content_type__model='item', object_id=self.id, user=user).first()
        return user_rating.score if user_rating else None


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.item}'
