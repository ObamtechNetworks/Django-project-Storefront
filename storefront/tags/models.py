from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    
class TaggedItem(models.Model):
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

# identifying the product being tagged, a poor way is importing product model and using as a foreign key
# best solution is ideinfitying using a generic way
# using: the Type (product, vidoe, article) and ID 
content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
object_id = models.PositiveIntegerField()  # limitation is when the object id is a GUID and not a psotive integer
# getting actual product, below helps to do this
content_object = GenericForeignKey()
