import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import ESGCompany, ESGMetric  # Replace 'api' with your app name


class Command(BaseCommand):
    help = 'Import ESG data from a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='The path to the ESG CSV file to import.'
        )

    def handle(self, *args, **options):
        file_path = options['csv_file']
        count = 0
        with open(file_path, newline='', encoding='latin1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                company, _ = ESGCompany.objects.get_or_create(
                    orgperm_id=int(row['orgpermid']),  # adjust for your actual headers
                    defaults={
                        'ticker': row['ticker'],
                        'name': row['comname'],
                        'isin': row.get('isin', None),
                        'siccode': row.get('siccode', None),
                    }
                )


                ESGMetric.objects.create(
                    company=company,
                    year=int(row['year']),
                    fieldid=int(row['fieldid']),
                    hierarchy=row['hierarchy'],
                    pillar=row['pillar'],
                    fieldname=row['fieldname'],
                    valuedate=datetime.strptime(row['valuedate'], '%Y-%m-%d').date(),
                    value=row['value'],
                    valuescore=float(row['valuescore'])
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully imported {count} ESG metric rows.'))
