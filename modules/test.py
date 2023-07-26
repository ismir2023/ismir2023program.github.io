import tutorials
import sys

# TODO Move the utils code to the same repo once everything is setup.
sys.path.append("..")
sys.path.append(".")

from utils import slack as slackUtils
from utils import zoom as zoomUtils
from modules.tutorials import Tutorials
from modules.papers import Papers
from modules.zoom_creator import ZoomCreator
from lbds import Lbds
from music import Music
from industry import Industry

# Uncomment below for zoom creation
# zoomCreator =  ZoomCreator("../../ISMIR-2022-Miniconf-Data/sitedata/events.csv")
# zoomCreator.setupZoomCalls(zoomUtils)

# Uncommnet below for tutorials slack setup
# tutObj = Tutorials("/Users/sg/ismir22-prod/miniconf-data/sitedata/events.csv", "/Users/sg/ismir22-prod/miniconf-data/sitedata/__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv")
# tutObj.setupSlackChannels(slackUtils)

##########################

# Uncommnet below for papers slack setup
# paperObj = Papers("/Users/sg/ismir22-prod/miniconf-data/sitedata/papers.csv")
# paperObj.setupSlackChannels(slackUtils)

# Uncommnet below for lbds slack setup
# lbdObj = Lbds("/Users/sg/ismir22-prod/miniconf-data/sitedata/lbds.csv")
# lbdObj.setupSlackChannels(slackUtils)

# Uncommnet below for music slack setup
# musicObj = Music("/Users/sg/ismir22-prod/miniconf-data/sitedata/music.csv")
# musicObj.setupSlackChannels(slackUtils)

# Uncommnet below for industry slack setup
industryObj = Industry("/Users/sg/ismir22-prod/miniconf-data/sitedata/industry.csv", "/Users/sg/ismir22-prod/miniconf-data/sitedata/__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv")
industryObj.setupSlackChannels(slackUtils)