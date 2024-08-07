from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model, ):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='pictures/profile_pictures')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# def default_image_path():
#     # Check if the profile picture exists in your static files
#     if os.path.exists(os.path.join(BASE_DIR, 'static', 'profilepic.jpg')):
#         return 'profilepic.jpg'
#     else:
#         return 'https://w7.pngwing.com/pngs/81/570/png-transparent-profile-logo-computer-icons-user-user-blue-heroes-logo-thumbnail.png'
#
