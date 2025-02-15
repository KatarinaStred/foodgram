import csv
import os

from django.core.management.base import BaseCommand, CommandError
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Tag

FILE_PATH = os.path.join(
    BASE_DIR,
    'data'
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(FILE_PATH, 'ingredients.csv')
            ) as file_csv:
                data = csv.DictReader(file_csv, delimiter=',')
                for row in data:
                    Ingredient.objects.create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit'],
                    )
                print('Файл ingredients.csv успешно импортирован')

            with open(
                os.path.join(FILE_PATH, 'tags.csv')
            ) as file_csv:
                data = csv.DictReader(file_csv, delimiter=',')
                for row in data:
                    Tag.objects.create(
                        name=row['name'],
                        slug=row['slug'],
                    )
                print('Файл tags.csv успешно импортирован')
        except Exception as error:
            raise CommandError(f'Произошла ошибка: {error}')
