from base64 import encode
from hashlib import sha3_256
from django.core.management.base import BaseCommand, CommandError
from parsing import models
import json
import pprint
import requests
from django.core.files.base import ContentFile


def goc_tag_cloud(data):
    return models.TagCloud.objects.get_or_create(foreign_id=data.get("id"), defaults={
        "foreign_id": data.get("id"),
        "foreign_path": data.get("url"),
        "tag": data.get("tag"),
    })[0]

def cou_recipe(data):
    return models.Recipe.objects.update_or_create(foreign_id=data.get("id"), defaults={
        "foreign_id": data.get("id"),
        "name": data.get("hed", ""),
    })[0]


def parse_react_strings(data, xfn, sfn):
    return sum(list(map(lambda x: [rec_strings(sfn(s)) for s in xfn(x)], data)), [])

def rec_strings(data):
    return "".join([
        value
        if isinstance(value, str)
        else rec_strings(value)
        for value
        in (data[1:] if isinstance(data, list) and len(data) > 1 else [])
        if isinstance(value, str)
        or isinstance(value, list)
    ])

def goc_image(url):
    try:
        return models.Image.objects.get(foreign_image=url)
    except models.Image.DoesNotExist:
        pass

    r = requests.get(url)

    if r.status_code != 200:
        return None
    
    filename = sha3_256(url.encode()).hexdigest() + "." + url.split(".")[-1]
    image = models.Image()
    image.foreign_image = url
    image.image.save(filename, ContentFile(r.content))
    image.save()
    return image
    

class Command(BaseCommand):
    # help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # for poll_id in options["poll_ids"]:
        items = models.FetchItem.objects.all()

        for item in items:
            print(f"Processing: {item.url}")
            lds = item.raw_json.get("lds", [])

            state = item.raw_json.get("preloadState", {})
            transformed = state.get("transformed", {})
            recipe = transformed.get("recipe", {})
            tagCloud = recipe.get("tagCloud", {})
            tags = list(map(lambda x: goc_tag_cloud(x), tagCloud.get("tags", [])))
            ingredient = parse_react_strings(
                recipe.get("ingredientGroups", []),
                lambda x: x.get("ingredients", []),
                lambda s: s.get("descriptionJsonMl", {})
            )
            instructions = parse_react_strings(
                recipe.get("instructions", []),
                lambda x: x.get("steps", []),
                lambda s: s.get("descriptionJsonMl", {})
            )
            description = rec_strings(
                recipe.get("body", []),
            )

            images = sum([obj.get("image") if isinstance(obj.get("image"), list) else [] for obj in lds], [])
            image_url = images[0] if len(images) > 0 else None

            if image_url is not None:
                image = goc_image(image_url)

            if recipe.get("id") is not None:
                recipe_obj = cou_recipe(recipe)
                recipe_obj.tag_clouds.set(tags)
                recipe_obj.fetch_item = item
                recipe_obj.ingredient = ingredient
                recipe_obj.instructions = instructions
                recipe_obj.description = description
                recipe_obj.images.set([image] if image is not None else [])
                recipe_obj.save()

            item.processed = True
            item.save()


        self.stdout.write(
            self.style.SUCCESS('Finish')
        )