from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError
import csv
from django.contrib.auth import get_user_model
from reprohack_hub.models import Event, Paper, Review, PaperReviewer
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Load initial data, the initial .csv files must be placed in the /initial_data folder with the name of events.csv, papers.csv and reviews.csv. \n Usage: \n ./manage.py load_initial -submitter [username]"

    def add_arguments(self, parser):
        parser.add_argument('-submitter', nargs=1, type=str, help="The username to be associated with initial uploads")

    def handle(self, *args, **options):
        print(f"Creating initial db data, objects will be assigned to admin user {options['submitter'][0]}")
        submitter_username = options['submitter'][0]
        self.load_initial_data(submitter_username)




    def load_initial_data(self, submitter_username):
        events_path = "initial_data/events.csv"
        papers_path = "initial_data/papers.csv"
        reviews_path = "initial_data/reviews.csv"

        submitter = get_user_model().objects.get(username=submitter_username)

        events = self.get_csv_dict(events_path)
        for row in events:
            event = Event.objects.create()
            event.creator = submitter
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
            paper = Paper.objects.create()
            paper.submitter = submitter
            # row["Name"]
            # row["Email address"]
            # row["GitHub username (optional)"]
            # row["Twitter handle (optional)"]
            # row["Can participants contact you directly regarding your paper?"]
            paper.title = row["Paper title"]
            paper.citation_txt = row["Paper citation"]
            paper.paper_url = row["Paper URL"]
            paper.data_url = row["Data URL"]
            paper.code_url = row["Code URL"]
            paper.why = row["Why should we attempt to reproduce this paper?"]
            if row["Can we  make the paper available for future ReproHacks?"] == "Yes":
                paper.review_availability = paper.ReviewAvailability.ALL
            else:
                paper.review_availability = paper.ReviewAvailability.EVENT_ONLY
            paper.archive = False
            # row["Would you like to receive a copy of any feedback on the paper?"]
            if row["Can feedback on your paper be made public?"] == "Yes":
                paper.public_reviews = True
            else:
                paper.public_reviews = False
            paper.save()

        reviews = self.get_csv_dict(reviews_path)
        for row in reviews:

            title = row["Which paper did you attempt?"]
            papers_query = Paper.objects.filter(title__contains=title)
            if papers_query.count() < 1:
                print(f"No paper \"{title}\" found, skipping review")
                continue

            review = Review.objects.create()
            review.paper = papers_query.first()

            if row["Did you manage to reproduce it?"] == "Yes":
                review.reproducibility_outcome = review.ReproducibilityOutcomes.FULLY_REPRODUCIBLE
            elif row["Did you manage to reproduce it?"] == "Almost":
                review.reproducibility_outcome = review.ReproducibilityOutcomes.PARTIALLY_REPRODUCIBLE
            else:
                review.reproducibility_outcome = review.ReproducibilityOutcomes.NOT_REPRODUCIBLE

            # row["Timestamp"]
            # row["Name of participant(s)"]
            review.reproducibility_description = row["Briefly describe the procedure followed / tools used to reproduce it."]
            review.reproducibility_rating = int(row["On a scale of 1 to 10, how much of the paper did you manage to reproduce?"])
            review.familiarity_with_method = row["Briefly describe your familiarity with the procedure/ tools used by the paper."]
            review.challenges = row["What were the main challenges you ran into (if any)?"]
            review.advantages = row["What were the positive features of this approach?"]
            review.comments_and_suggestions = row["Any other comments / suggestions on the reproducibility approach?"]
            review.documentation_rating = int(row["How well was the material documented?"])
            review.documentation_cons = row["How could the documentation be improved?"]
            review.documentation_pros = row["What did you like about the documentation?"]
            review.method_familiarity_rating = int(row["After attempting to reproduce, how familiar do you feel with code and method used in the paper?"])
            review.transparency_suggestions = row["Any suggestions on how the analysis could be made more transparent?"]
            review.method_reusability_rating = int(row["Rate the project on reusability of the material"])
            # row["Are materials clearly covered by a permissive enough license to build on?"]
            review.reusability_suggestions = row["Any suggestions on how the project could be more reusable?"]
            review.general_comments = row["Any Final Comments:"]
            # row["Contact email"]
            # row["Attach document with additional review comments"]
            review.public_review = True
            review.save()

            PaperReviewer.objects.create(review=review, user=submitter)

    def get_csv_dict(self, path):
        out_list = []
        with open(path) as events_file:
            reader = csv.DictReader(events_file)
            for row in reader:
                out_list.append(row)


        return out_list
