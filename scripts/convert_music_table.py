import pandas as pd
import re
import sys

authors_list = []
affils_list = []
keywords_list = []
session_list = []
# with open('../pre_parse_ISMIR2020_papers.csv', 'r') as f:
orig_csv = pd.read_csv('../static/csv/ISMIR music program _ Streaming ready submission (Responses) - Form Responses 1 for site.csv')

# Rework authors, affiliations, subject areas

# for index, row in orig_csv.iterrows():


new_csv = pd.DataFrame(
    {"UID": orig_csv['Submission number '],
    # "type": orig_csv['Content Type'],
    "title": [ "".join((title, ': The Voice of Santur with Audience Participation')) if 'Sunrise' in title else title for title in orig_csv["Title of the piece"]],
    "abstract": orig_csv["Abstract of the piece. This abstract is going to be displayed on the ISMIR music program page. (150-250 words)"],
    "first_name": orig_csv["Given name"],
    "last_name": orig_csv["Family name"],
    "affiliation": orig_csv["University, Corporate / Institutional affiliation(s)"],
    "bio": orig_csv["Short bio (100-200 words)"],
    "web_link": orig_csv["Link to your website (optional)"],
    "session": orig_csv["Session Number"],
    "yt_id": [link.split('/')[-1] if isinstance(link, str) else link for link in orig_csv["YouTube link"]],
    "bb_id": [link.split('/')[-1] if isinstance(link, str) else link for link in orig_csv["Bilibili link"]],
    "db_link": orig_csv["Dropbox link"],
    "authors": orig_csv["Authors"],
    "still_image": orig_csv["Still image (for audio-only submissions). "],
    "release_consent": [1 if isinstance(x, str) else 0 for x in orig_csv["Consent"]],
})

print(new_csv)
new_csv.to_csv('../sitedata/music.csv', index=False)
