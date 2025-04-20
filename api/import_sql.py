import os
import django
import csv
from datetime import datetime
from django.db import connection, transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terravest_website.settings')  # Replace with your actual settings module
django.setup()

BATCH_SIZE = 1000
TOTAL_ROWS = 15675979  # Total number of rows in the CSV file

def process_batch(batch, cursor, processed_rows):
    """
    Process a batch of rows for ESG data using ON CONFLICT for efficient upserts.
    """
    company_inserts = []
    metric_inserts = []

    for row in batch:
        # Prepare data for ESGCompany
        company_inserts.append((
            row['orgpermid'], row['ticker'], row['comname'], row['isin'], row['siccode']
        ))

        # Prepare data for ESGMetric
        metric_inserts.append((
            row['orgpermid'], row['year'], row['fieldid'], row['hierarchy'], row['pillar'],
            row['fieldname'], row['value'], row['valuescore']
        ))

    # Perform bulk upserts for ESGCompany
    if company_inserts:
        cursor.executemany("""
            INSERT INTO api_esgcompany (orgperm_id, ticker, name, isin, siccode)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (orgperm_id) DO UPDATE
            SET ticker = EXCLUDED.ticker,
                name = EXCLUDED.name,
                isin = EXCLUDED.isin,
                siccode = EXCLUDED.siccode;
        """, company_inserts)

    # Perform bulk upserts for ESGMetric
    if metric_inserts:
        cursor.executemany("""
            INSERT INTO api_esgmetric (company_id, year, fieldid, hierarchy, pillar, fieldname, value, valuescore)
            VALUES (
                (SELECT id FROM api_esgcompany WHERE orgperm_id = %s),
                %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (company_id, year, fieldid) DO UPDATE
            SET hierarchy = EXCLUDED.hierarchy,
                pillar = EXCLUDED.pillar,
                fieldname = EXCLUDED.fieldname,
                value = EXCLUDED.value,
                valuescore = EXCLUDED.valuescore;
        """, metric_inserts)

    # Update progress
    processed_rows += len(batch)
    print(f"Processed {processed_rows}/{TOTAL_ROWS} rows ({(processed_rows / TOTAL_ROWS) * 100:.2f}%)")
    return processed_rows

def import_esg_data_sql(csv_file_path):
    """
    Import ESG data from a CSV file into the database using raw SQL.
    Processes data in batches for efficiency.
    """
    with open(csv_file_path, newline='', encoding='latin1') as csvfile:  # Change encoding to 'latin1'
        reader = csv.DictReader(csvfile)
        batch = []
        processed_rows = 0

        with connection.cursor() as cursor:
            with transaction.atomic():  # Use a single transaction for all operations
                for row in reader:
                    batch.append(row)
                    if len(batch) >= BATCH_SIZE:
                        processed_rows = process_batch(batch, cursor, processed_rows)
                        batch = []  # Clear the batch after processing

                # Process any remaining rows
                if batch:
                    processed_rows = process_batch(batch, cursor, processed_rows)

if __name__ == "__main__":
    # Replace 'path/to/your/csvfile.csv' with the actual path to your CSV file
    csv_file_path = '/Users/palashgandhi/Documents/GitHub/terravest-website/data/data.csv'
    import_esg_data_sql(csv_file_path)
    print("Data import completed successfully.")