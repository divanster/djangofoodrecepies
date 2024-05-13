from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Item(models.Model):

    def __str__(self):
        return self.item_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    # item_image = models.ImageField(upload_to='') better for image storage with validation and upload function
    item_image = models.CharField(max_length=500,
                                  default='https://media.istockphoto.com/id/1426890025/es/foto/la-pizza-de-la-que-te'
                                          '-olvidaste-durante-una-semana-y-se-puso-mohosa.jpg?s=612x612&w=0&k=20&c'
                                          '=r0cHrYxEjoLUoSz9VQCglgXc6Win_fFu-fjDwWfoPu4=')

    def get_absolute_url(self):
        return reverse("food:detail", kwargs={"pk": self.pk})
