import csv
from django.core.management.base import BaseCommand
from reviews.models import Genre_title, Title, Genre
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/genre_title.csv", encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                Genre_title.objects.create(
                    id=row['id'],
                    title_id=Title.objects.get_or_create(id=row['title_id']),
                    genre_id=Genre.objects.get_or_create(id=row['genre_id'])
                )
