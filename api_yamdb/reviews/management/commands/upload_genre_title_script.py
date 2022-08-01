import csv
from django.core.management.base import BaseCommand
from reviews.models import Genre_title, Titles, Genre


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/genre_title.csv",  encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            Genre_title.objects.bulk_create([
                Genre_title(
                    id=line['id'],
                    title_id=Titles.objects.get_or_create(id=line['title_id']),
                    genre_id=Genre.objects.get_or_create(id=line['genre_id'])
                ) for line in reader
            ])
