import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand  # , CommandError
from django.db import IntegrityError
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Tag

FILE_PATH = os.path.join(
    BASE_DIR,
    'data'
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = datetime.now()
        with open(
            os.path.join(FILE_PATH, 'ingredients.csv')
        ) as file_csv:
            data = csv.reader(file_csv)
            for row in data:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit'],)
                    if not created:
                        print(f'Ингредиент {obj} уже есть в базе.')
                except IntegrityError as err:
                    print(f'Ошибка в строке {row}: {err} по ингредиентам.')
            print('Файл ingredients.csv успешно импортирован')

        with open(
            os.path.join(FILE_PATH, 'tags.csv')
        ) as file_csv:
            data = csv.reader(file_csv)
            for row in data:
                try:
                    obj, created = Tag.objects.get_or_create(
                        name=row['name'],
                        slug=row['slug'])
                    if not created:
                        print(f'Тег {obj} уже есть в базе.')
                except IntegrityError as err:
                    print(f'Ошибка в строке {row}: {err} по тегам.')
            print('Файл tags.csv успешно импортирован')

        end_time = datetime.now()
        duration = end_time - start_time
        minutes = duration.seconds // 60
        seconds = duration.seconds % 60

        self.stdout.write(
            self.style.SUCCESS(
                (f'Данные были загружены в БД за '
                 f'{minutes} {seconds}')
            )
        )
