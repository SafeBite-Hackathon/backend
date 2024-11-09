from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.postgres.fields import ArrayField


class FetchItemStatus(models.IntegerChoices):
    pending = (0, "Pending")
    parsing = (1, "Parsing")
    finished = (2, "Finished")
    error = (3, "Error")


class FetchItem(models.Model):
    url = models.CharField(max_length=4096, unique=True)
    raw_json = models.JSONField(null=True)
    status = models.PositiveSmallIntegerField(choices=FetchItemStatus.choices, default=FetchItemStatus.pending)
    processed = models.BooleanField(default=False)

    def __str__(obj):
        return f"{'Processed' if obj.processed else 'Not processed'} - {obj.id} - {obj.url}"


class Image(models.Model):
    foreign_image = models.CharField(max_length=4096, unique=True)
    image = models.ImageField(upload_to="images/")
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(250, 180)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(obj):
        return obj.foreign_image


class TagCloud(models.Model):
    foreign_id = models.CharField(max_length=64, unique=True)
    foreign_path = models.CharField(max_length=4096)
    tag = models.CharField(max_length=256)

    def __str__(obj):
        return obj.tag
    
class Tag(models.Model):
    foreign_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    parent = models.ForeignKey("parsing.Tag", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(obj):
        return obj.name


class Recipe(models.Model):
    foreign_id = models.CharField(max_length=64, unique=True)
    fetch_item = models.ForeignKey(FetchItem, on_delete=models.SET_NULL, null=True, blank=True)
#     foreign_url = models.CharField(max_length=4096)
    name = models.CharField(max_length=1024, default="")
    description = models.TextField(default="")

#     alternative_headline = models.TextField(default="")
#     article_body = models.TextField(default="")
#     cook_time = models.CharField(max_length=256, default="")
#     description = models.TextField(default="")
#     headline = models.TextField(default="")
#     total_time = models.CharField()
    
    images = models.ManyToManyField(Image)

    tag_clouds = models.ManyToManyField(TagCloud)
    # tags = models.ManyToManyField(Tag)

    ingredient = ArrayField(models.CharField(max_length=2048), default=list)
    instructions = ArrayField(models.CharField(max_length=2048), default=list)

    def __str__(obj):
        return obj.name
