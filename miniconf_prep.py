from scripts.calendar_csv2ics import calendar_csv2ics
from scripts.calendar_ics2json import calendar_ics2json
from scripts.remove_private_details import remove_author_contacts
from modules.tutorials import Tutorials
from modules.papers import Papers
from modules.zoom_creator import ZoomCreator
from modules.lbds import Lbds
from modules.music import Music
from modules.industry import Industry
import argparse
import os


# Prepare for tutorials
# 1. Go to /static/tutorials
# 2. Update the tutorial content as seen in the tut_X.md files.
# 3. Add/Remove tut_X.md files as necessary. Make sure they are consecutive in number

useDummyValues = True

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Prep Script")

    parser.add_argument(
        "--path",
        help="Pass the path of directory containing the master data.",
        required=False)


    parser.add_argument(
        "--prod",
        help="set this value as true if we want to run on prod data.",
        default=False)

    #### Possible actions ####
    # setup-zoom
    # setup-tutorial
    # setup-papers
    # setup-lbd
    # setup-music
    # setup-sponsors
    # remove-author-email
    # prepare-calendar
    # process-new-users

    parser.add_argument(
        "--action",
        help="set this value to one of the possible actions: setup-zoom, setup-tutorial, setup-papers, setup-lbd, setup-music, setup-sponsors, remove-author-email, prepare-calendar, process-new-users", required=True)

    args = parser.parse_args()
    return args

# Step1: Create Slack channels and zoom meetings
def setupZoom(eventsCsvFile):
    zoomCreator = ZoomCreator(eventsCsvFile, useDummyValues)
    zoomCreator.setupZoomCalls(zoomUtils)

def setupTutorials(eventsCsvFile, registrtionDataCsvFile):
    tutObj = Tutorials(eventsCsvFile, registrtionDataCsvFile, useDummyValues)
    tutObj.setupSlackChannels(slackUtils)

def setupPapers(papersCsvFile):
    paperObj = Papers(papersCsvFile, useDummyValues)
    paperObj.setupSlackChannels(slackUtils)

def setupLbds(lbdCsvFile):
    lbdObj = Lbds(lbdCsvFile, useDummyValues)
    lbdObj.setupSlackChannels(slackUtils)

def setupMusic(musicCsvFile):
    musicObj = Music(musicCsvFile, useDummyValues)
    musicObj.setupSlackChannels(slackUtils)

def setupSponsors(industryCsvFile, registrtionDataCsvFile):
    industryObj = Industry(industryCsvFile, registrtionDataCsvFile, useDummyValues)
    industryObj.setupSlackChannels(slackUtils)

def removeAuthorEmails():
    remove_author_contacts()


if __name__ == "__main__":
    args = parse_arguments()
    data_path = args.path
    useDummyValues = not args.prod
    action = args.action

    if (action is None):
        raise Exception("--action is missing. Possible values are setup-zoom, setup-tutorial, setup-papers, setup-lbd, setup-music, setup-sponsors, remove-author-email, prepare-calendar", "process-new-users")

    if 'setup' in action or 'process' in action:
        if(data_path is None):
            raise Exception("--path for the root directory for data is missing")
        from utils import slack as slackUtils
        from utils import zoom as zoomUtils

    if (action == "setup-zoom"):
        setupZoom(os.path.join(data_path, "events.csv"))

    elif (action == "setup-tutorials"):
        setupTutorials(os.path.join(data_path, "events.csv"), os.path.join(data_path, "__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv"))

    elif (action == "setup-papers"):
        setupPapers(os.path.join(data_path, "papers.csv"))

    elif (action == "setup-lbd"):
        setupLbds(os.path.join(data_path, "lbds.csv"))

    elif (action == "setup-music"):
        setupMusic(os.path.join(data_path, "music.csv"))

    elif (action == "setup-sponsors"):
        setupSponsors(os.path.join(data_path, "industry.csv"), os.path.join(data_path, "__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv"))

    elif (action == "process-new-users"):
        # First setup tutorials.
        setupTutorials(os.path.join(data_path, "events.csv"), os.path.join(data_path, "__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv"))
        # Next setup sponsors.
        setupSponsors(os.path.join(data_path, "industry.csv"), os.path.join(data_path, "__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv"))

    elif (action == "remove-author-email"):
        removeAuthorEmails()

    elif (action == "prepare-calendar"):
        # Step3: Prepare for calendar
        # If links from schedule are not redirecting to the right page, check this code
        calendar_csv2ics()
        calendar_ics2json()





