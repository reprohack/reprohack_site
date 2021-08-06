from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError
import csv
from django.contrib.auth import get_user_model
from reprohack_hub.models import Event, Paper, Review
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Load initial data"

    def handle(self, *args, **options):
        print("Creating initial db data")
        admin_user = get_user_model().objects.create(username="rhadmin",
                                                     email="reprohack-hub@sheffield.ac.uk",
                                                     is_superuser=True,
                                                     is_staff=True)
        admin_user.set_password("T47BfFovEAvTsJiKp3A")
        admin_user.save()

        self.load_initial_data()


    def get_csv_dict(self, path):
        out_list = []
        with open(path) as events_file:
            reader = csv.DictReader(events_file)
            for row in reader:
                out_list.append(row)


        return out_list

    def load_initial_data(self):
        events_path = "data/events.csv"
        papers_path = "data/papers.csv"
        reviews_path = "data/reviews.csv"

        admin = get_user_model().objects.get(username="rhadmin")

        events = self.get_csv_dict(events_path)
        for row in events:
            event = Event.objects.create()
            event.creator = admin
            event.host = ""
            event.title = row["title"]
            event.is_initial_upload = True
            event.start_time = datetime.strptime(row["date"] + " " + row["start_time"], "%Y-%m-%d %H:%M")
            event.end_time = datetime.strptime(row["date"] + " " + row["end_time"], "%Y-%m-%d %H:%M")
            event.city = row["city"]
            event.country = row["country"]
            event.address1 = row["address"]
            event.registration_url = row["url"]
            event.event_coordinates = ",".join([row["lat"], row["lon"]])
            event.save()



        papers = self.get_csv_dict(papers_path)
        for row in papers:
            print(row)

        reviews = self.get_csv_dict(reviews_path)
        for row in reviews:
            print(row)
