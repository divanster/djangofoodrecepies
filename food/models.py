from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Item(models.Model):

    def __str__(self):
        return self.item_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_image = models.CharField(max_length=500,
                                  default='https://media.istockphoto.com/id/1426890025/es/foto/la-pizza-de-la-que-te'
                                          '-olvidaste-durante-una-semana-y-se-puso-mohosa.jpg?s=612x612&w=0&k=20&c'
                                          '=r0cHrYxEjoLUoSz9VQCglgXc6Win_fFu-fjDwWfoPu4=')
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("food:detail", kwargs={"pk": self.pk})

    def increment_views(self):
        self.views += 1
        self.save()

    def average_rating(self):
        ratings = Rating.objects.filter(item=self)
        if ratings.exists():
            return sum(r.value for r in ratings) / len(ratings)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    # item_image = models.ImageField(upload_to='') better for image storage with validation and upload function
