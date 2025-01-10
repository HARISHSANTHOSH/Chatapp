import pandas as pd
from django.core.management.base import BaseCommand

from chatapp import controllers


class Command(BaseCommand):
    help = "Import user data from CSV and generate embeddings"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        # Read the CSV file
        try:
            data = pd.read_csv(csv_file)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV: {e}"))
            return

        # Iterate through the rows and add data to the database
        for index, row in data.iterrows():
            user_id = (
                index + 1
            )  # Or use another unique identifier for your user_id
            name = row["name"]
            email = row["email"]
            phone_number = row["phone_number"]
            address = row["address"]

            # Call the function to add user data and generate embeddings
            try:
                controllers.add_user_data(
                    user_id=user_id,
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    address=address,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"User {name} added successfully")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error adding user {name}: {e}")
                )
