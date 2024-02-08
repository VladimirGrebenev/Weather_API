import csv
from django.core.management.base import BaseCommand
from weather.models import City


class Command(BaseCommand):
    help = 'Import cities from cities.csv'

    def handle(self, *args, **options):
        with open('cities.csv', 'r') as file:
            reader = csv.reader(file)
            cities_count = 0
            for row in reader:
                name = row[0]
                lat = float(row[1])
                lon = float(row[2])
                City.objects.create(name=name, lat=lat, lon=lon)
                cities_count += 1
        self.stdout.write(self.style.SUCCESS(f'Cities imported successfully ({cities_count} cities)'))
