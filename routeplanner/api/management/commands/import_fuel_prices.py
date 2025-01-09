import os
from django.core.management.base import BaseCommand
from api.models import FuelPrice

class Command(BaseCommand):
    help = "Import fuel prices from CSV"

    def handle(self, *args, **kwargs):
        # Get the absolute path to the CSV file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '../../../../fuel-prices-for-be-assessment.csv')

        # Open and read the CSV file
        with open(file_path, 'r') as file:
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                FuelPrice.objects.create(
                    truckstop_name=row['Truckstop Name'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    retail_price=float(row['Retail Price'])
                )
        self.stdout.write(self.style.SUCCESS("Fuel prices imported successfully."))
