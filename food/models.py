from django.db import models


class Item(models.Model):

    def __str__(self):
        return self.item_name

    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    # item_price = models.DecimalField(max_digits=10, decimal_places=2) better for prices
    # item_image = models.ImageField(upload_to='') better for image storage with validation and upload function
    item_image = models.CharField(max_length=500, default='https://media.istockphoto.com/id/1426890025/es/foto/la-pizza-de-la-que-te-olvidaste-durante-una-semana-y-se-puso-mohosa.jpg?s=612x612&w=0&k=20&c=r0cHrYxEjoLUoSz9VQCglgXc6Win_fFu-fjDwWfoPu4=')


