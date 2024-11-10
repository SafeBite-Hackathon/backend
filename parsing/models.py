from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.postgres.fields import ArrayField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


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

    
class Tag(MPTTModel):
    foreign_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(obj):
        return obj.name
    
    class MPTTMeta:
        order_insertion_by = ['name']


class Recipe(models.Model):
    foreign_id = models.CharField(max_length=64, unique=True)
    fetch_item = models.ForeignKey(FetchItem, on_delete=models.SET_NULL, null=True, blank=True)
#     foreign_url = models.CharField(max_length=4096)
    name = models.CharField(max_length=1024, default="")
    description = models.TextField(default="")
    rating = models.FloatField(default=0)
    active_time = models.CharField(max_length=128, default="")
    prep_time = models.CharField(max_length=128, default="")
    total_time = models.CharField(max_length=128, default="")
    serving_size = models.CharField(max_length=128, default="")

#     alternative_headline = models.TextField(default="")
#     article_body = models.TextField(default="")
#     cook_time = models.CharField(max_length=256, default="")
#     description = models.TextField(default="")
#     headline = models.TextField(default="")
#     total_time = models.CharField()
    
    images = models.ManyToManyField(Image)
    tags = models.ManyToManyField(Tag)

    ingredient = ArrayField(models.CharField(max_length=2048), default=list)
    instructions = ArrayField(models.CharField(max_length=2048), default=list)

    def __str__(obj):
        return obj.name


class DietGoal(models.TextChoices):
    get_inspiration = ("get_inspiration", "Get inspiration")
    eat_healthy = ("eat_healthy", "Eat healthy")
    loose_weight = ("loose_weight", "Loose weight")
    build_muscles = ("build_muscles", "Build muscles")


class DietType(models.TextChoices):
    i_eat_everything = ("i_eat_everything", "I eat everything")
    pescatarian = ("pescatarian", "Pescatarian")
    vegetarian = ("vegetarian", "Vegetarian")
    vegan = ("vegan", "Vegan")


class MealTime(models.TextChoices):
    breakfast = ("breakfast", "Breakfast")
    brunch = ("brunch", "Brunch")
    dinner = ("dinner", "Dinner")
    lunch = ("lunch", "Lunch")


class MealFilter(models.Model):
    meal_time = models.CharField(max_length=64, choices=MealTime.choices)
    diet_type = models.CharField(max_length=64, choices=DietType.choices)
    diet_goal = models.CharField(max_length=64, choices=DietGoal.choices)
    tags = models.ManyToManyField(Tag)

    class Meta:
        unique_together = ['meal_time', 'diet_type', 'diet_goal']
    
    def __str__(obj):
        return "{} - {} - {}".format(
            obj.get_meal_time_display(),
            obj.get_diet_type_display(),
            obj.get_diet_goal_display(),
        )


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_weight = models.PositiveIntegerField(null=True, blank=True)
    goal_weight = models.PositiveIntegerField(null=True, blank=True)
    diet_goal = models.CharField(max_length=64, choices=DietGoal.choices, null=True, blank=True)
    diet_type = models.CharField(max_length=64, choices=DietType.choices, null=True, blank=True)
    allegries = models.ManyToManyField(Tag, related_name="allergic_users")
    preferences = models.ManyToManyField(Tag, related_name="prerence_users")
