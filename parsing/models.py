from django.db import models


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


# class Image(models.Model):
#     foreign_image = models.CharField(max_length=4096, unique=True)
#     local_image = models.ImageField(upload_to="images/", null=True, blank=True)


# class Tag(models.Model):
#     foreign_id = models.CharField(max_length=64)
#     foreign_url = models.CharField(max_length=4096)
#     tag = models.CharField(max_length=256)


# class Recipe(models.Model):
#     fetch_item = models.ForeignKey(FetchItem, on_delete=models.SET_NULL, null=True, blank=True)
#     foreign_url = models.CharField(max_length=4096)

#     alternative_headline = models.TextField(default="")
#     article_body = models.TextField(default="")
#     cook_time = models.CharField(max_length=256, default="")
#     description = models.TextField(default="")
#     headline = models.TextField(default="")
#     total_time = models.CharField()
    
#     images = models.ManyToManyField(Image)
#     tags = models.ManyToManyField(Tag)


# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     text = models.TextField()


# class RecipeInstructions(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     text = models.TextField()
