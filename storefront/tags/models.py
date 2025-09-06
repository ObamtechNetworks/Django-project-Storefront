from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        
        return TaggedItem.objects\
        .select_related('tag')\
        .filter(
            content_type=content_type,
            object_id=obj_id
        )

class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.label


class TaggedItem(models.Model):
    objects = TaggedItemManager() # custom manager to get tags for an object
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # know what type of item (product? video? article? whatever)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # id of the target object (primary key)
    object_id = models.PositiveIntegerField()
    # getting actual object the tagged item is related to
    content_object = GenericForeignKey()
