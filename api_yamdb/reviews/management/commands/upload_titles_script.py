import csv
from django.core.management.base import BaseCommand
from reviews.models import Titles, Categories



class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/titles.csv",  encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            Titles.objects.bulk_create([
                Titles(
                    id=line['id'],
                    name=line['name'],
                    year=line['year'],
                    category=Categories.objects.get(pk=int(line['category']))
                ) for line in reader
            ])
