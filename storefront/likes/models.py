from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # to idenitfy the object being liked, we need, the content_type, ID and GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # limitation is when the object id is a GUID and not a psotive integer
    # getting actual product, below helps to do this
    content_object = GenericForeignKey()
