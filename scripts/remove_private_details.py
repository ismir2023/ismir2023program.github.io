import os
import pandas as pd
from shutil import copyfile
def remove_author_contacts(in_dir='../miniconf-data/sitedata/', out_dir='sitedata'):
    os.makedirs(out_dir, exist_ok=True)

    print('Removing author details from events.csv ')
    f = pd.read_csv(os.path.join(in_dir, 'events.csv'))
    f.drop('organiser_emails', axis=1, inplace=True)
    f.to_csv(os.path.join(out_dir, 'events.csv'), index=False)

    print('Removing author details from papers.csv ')
    f = pd.read_csv(os.path.join(in_dir, 'papers.csv'))
    f.drop('author_emails', axis=1, inplace=True)
    f.drop('primary_email', axis=1, inplace=True)
    f.to_csv(os.path.join(out_dir, 'papers.csv'), index=False)

    print('Removing author details from lbds.csv ')
    f = pd.read_csv(os.path.join(in_dir, 'lbds.csv'))
    f.drop('author_emails', axis=1, inplace=True)
    f.drop('primary_email', axis=1, inplace=True)
    f.to_csv(os.path.join(out_dir, 'lbds.csv'), index=False)

    print('Removing author details from industry.csv ')
    f = pd.read_csv(os.path.join(in_dir, 'industry.csv'))
    f.drop('registered_emails', axis=1, inplace=True)
    f.to_csv(os.path.join(out_dir, 'industry.csv'), index=False)

    print('Removing author details from music.csv ')
    f = pd.read_csv(os.path.join(in_dir, 'music.csv'))
    f.drop('author_emails', axis=1, inplace=True)
    f.drop('primary_email', axis=1, inplace=True)
    f.to_csv(os.path.join(out_dir, 'music.csv'), index=False)

    print('Removing author details from jobs.csv ')
    copyfile(os.path.join(in_dir, 'jobs.csv'), os.path.join(out_dir, 'jobs.csv'))


if __name__ == "__main__":
    remove_author_contacts()