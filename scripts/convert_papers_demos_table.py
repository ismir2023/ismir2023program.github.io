import pandas as pd
import re
import sys
import math

authors_list = []
affils_list = []
keywords_list = []
session_list = []
slack_channel_list = []
slack_name_list = []
day_list = []
slot_list = []
poster_code_list = []
yt_id_list = []
bb_id_list = []

authors_list_lbds = []
affils_list_lbds = []
emails_list_lbds = []

orig_csv = pd.read_csv('../static/csv/ISMIR2020 papers - pre_parse_ISMIR2020_papers.csv')
schedule_csv = pd.read_csv('../static/csv/Schedule - Paper (Preliminary) - Schedule - Paper (Preliminary).csv')

orig_csv_lbds = pd.read_csv('../static/csv/2020-ISMIR-LBD-Submissions - Sheet1.csv')

print('Min or max keywords? [mM]')
key_choice = str(input())
if key_choice not in ['m', 'M']:
    sys.exit('Chooose one of the options above')

articles = ['a', 'an', 'of', 'the', 'for', 'and', 'nor', 'but', 'or', 'yet',
    'so', 'at', 'by', 'from', 'with', 'without', 'to', 'on', 'via', 'in', 'vs']

capital_exceptions = ['DJ', 'LSTM-HSMM', 'SuPP', 'MaPP:', 'POP909:', 'PIANOTREE',
    'VAE', 'VAE:', 'MIR', 'MIR:', 'ASAP', 'Tag2Risk:', 'BebopNet:', 'SketchNet', 'BTS',
    'ARMY', 'Human-AI', 'Song/Artist', 'MIDI', 'MusPy', 'GrooveToolbox', 'EEG',
    'Fadernets', 'CONLON', 'DRUMGAN', 'JavaScript', 'dMelodies',
    'Ethno-Music-Ontology', 'AI', 'AI-composed', 'COVID-19', 'Mix-To-Track',
    'OLAF:', 'RNNs', 'TuneIn:', 'VGGish', 'PyTSMod:', 'MEI-encoded',
    'MIREX']

def title_except(s, no_cap_list, unique_cap_list):
    word_list = re.split(' ', s)       # re.split behaves as expected
    # print(word_list)
    for i, word in enumerate(word_list):
        check = word.lower()
        if check in no_cap_list:
            word_list[i] = check
    if word_list[0] in unique_cap_list: # First always capitalized logic
        final = [word_list[0]]
    elif word_list[0] != '' and word_list[0][0] == '"':
        final = [word_list[0][0] + word_list[0][1:].capitalize()] if word_list[0][1:] not in unique_cap_list else [word_list[0]]
    else:
        final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        if word in unique_cap_list:
            final.append(word)
        elif word != '' and word[0] == '"': #catch words that should be capitalized after a quote
            final.append(word[0] + word[1:].capitalize()) if word[1:] not in unique_cap_list else final.append(word)
        else:
            final.append(word if word in no_cap_list else word.capitalize())
    # print(final)
    return " ".join(final)

def extract_author_affil(row, cell_ref):
    authors = []
    affils = []
    author_affil = row[cell_ref].split('; ')
    for pair in author_affil:
        # print(pair)
        if pair[-1] == '*': # asterisk may need to be handled differently
            pair = pair[:-2]
        else:
            pair = pair[:-1]
        ps = pair.split(' (')
        # print(ps)
        authors.append(ps[0])
        affils.append(ps[1])
    authors = "|".join(authors)
    affils = "|".join(affils)
    return authors, affils

def extract_emails(row, cell_ref):
    emails = []
    raw_emails = row[cell_ref].split('; ')
    for m in raw_emails:
        m = m[:-1] if m[-1] == '*' else m
        emails.append(m)
    return emails

# Rework authors, affiliations, subject areas

for index, row in orig_csv.iterrows():

    session_num = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Session"].values[0]
    slack_channel = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Slack URL"].values[0]
    day = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Day"].values[0]
    slot = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Slot"].values[0]
    slack_name = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Slack Channel"].values[0]
    poster_code = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Poster code"].values[0]
    yt_link = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["Youtube"].values[0]
    bb_link = schedule_csv[schedule_csv["Paper ID"] == row["Paper ID"]]["bilibili"].values[0]
    print(f'{type(yt_link)} | {type(bb_link)}')
    if not isinstance(yt_link, str) and math.isnan(yt_link):
        yt_id = yt_link
    else:
        yt_id = yt_link.split('/')[-1]
    if not isinstance(bb_link, str) and math.isnan(bb_link):
        bb_id = bb_link
    else:
        bb_id = bb_link.split('/')[-2]

    print(f'{yt_link} : {yt_id} | {bb_link} : {bb_id}')
    # session_num = math.ceil(session_num / 2)
    if key_choice == 'm':
        primary_sub = [row['Primary Subject Area'].split(' -> ')[1]]
        secondary_sub = [[x.split(' -> ')[1]] for x in row['Secondary Subject Areas'].split('; ')] if not pd.isnull(row['Secondary Subject Areas']) else None
    else:
        primary_sub = row['Primary Subject Area'].split(' -> ')
        secondary_sub = [x.split(' -> ') for x in row['Secondary Subject Areas'].split('; ')] if not pd.isnull(row['Secondary Subject Areas']) else None
    secondary_sub = [term for sub in secondary_sub for term in sub] if secondary_sub else None

    keywords = primary_sub + secondary_sub if secondary_sub else primary_sub
    keywords = list(dict.fromkeys(keywords))
    keywords = "|".join(keywords)

    authors, affils = extract_author_affil(row, 'Authors')

    authors_list.append(authors)
    affils_list.append(affils)
    keywords_list.append(keywords)
    session_list.append(session_num)
    slack_channel_list.append(slack_channel)
    slack_name_list.append(slack_name)
    day_list.append(day)
    slot_list.append(slot)
    poster_code_list.append(poster_code)
    yt_id_list.append(yt_id)
    bb_id_list.append(bb_id)

    # print(keywords, '\n')

for index, row in orig_csv_lbds.iterrows():
    authors, affils = extract_author_affil(row, 'Authors')
    emails = extract_emails(row, 'Author Emails')
    authors_list_lbds.append(authors)
    affils_list_lbds.append(affils)
    emails_list_lbds.append(emails)


    # print(author_affil)
new_csv = pd.DataFrame(
    {"UID": poster_code_list,
    # "type": orig_csv['Content Type'],
    "title": [title_except(x, articles, capital_exceptions) for x in orig_csv['Paper Title']],
    "abstract": orig_csv['Abstract'],
    "primary_author": orig_csv['Primary Contact Author Name'],
    "primary_email": orig_csv['Primary Contact Author Email'],
    "session": session_list,
    "authors": authors_list,
    "affiliations": affils_list,
    "keywords": keywords_list,
    "channel_url": slack_channel_list,
    "channel_name": slack_name_list,
    "day": day_list,
    "slot": slot_list,
    "pic_id": orig_csv['Paper ID'],
    "yt_id": yt_id_list,
    "bb_id": bb_id_list,
    # "poster_code": poster_code_list,
})

new_csv_lbds = pd.DataFrame(
    {"UID": orig_csv_lbds['Paper ID'],
    "title": [title_except(x, articles, capital_exceptions) for x in orig_csv_lbds['Paper Title']],
    "abstract": orig_csv_lbds['Abstract'],
    "primary_author": orig_csv_lbds['Primary Contact Author Name'],
    "primary_email": orig_csv_lbds['Primary Contact Author Email'],
    "session": [0] * len(orig_csv_lbds['Paper ID']),
    "authors": authors_list_lbds,
    "affiliations": affils_list_lbds,
    "author_emails": emails_list_lbds,
})
# UID   title   authors session	day	abstract	keywords
# print(orig_csv)
# for i, row in new_csv.iterrows():
#     print(row[["session", "slot"]])
new_csv.to_csv('../sitedata/papers.csv', index=False)
# new_csv_lbds.to_csv('../sitedata/lbds.csv', index=False)
