import argparse
import csv
import json

import yaml
from requests import sessions

import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

# 1) First create a Slack App:
# https://api.slack.com/apps?new_app=1
# Setup authentication with the following list of scopes to obtain your OAuth Access Token "xoxp-...":
# - admin
# - channels:read
# - channels:write
# - chat:write
# - search:read
# - users:read
# https://api.slack.com/authentication/basics
# 2) Install your Slack app to your Slack workspace.
# 3) Run this script in a terminal with: 
# SLACK_OAUTH_TOKEN="xoxp-..." python make_slack_channels_presentations.py

channels_url = "https://ismir2020.slack.com/archives/"

slack_token = os.environ["SLACK_OAUTH_TOKEN"]
client = WebClient(token=slack_token)


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    # parser.add_argument("--list", default="../sitedata/papers.csv", help="Papers or LBDs CSV")
    parser.add_argument("--list", default="../sitedata/lbds.csv", help="Papers or LBDS CSV")
    parser.add_argument("--test", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    csvfile = csv.DictReader(open(args.list))
    fieldnames = csvfile.fieldnames;
    print('fieldnames',fieldnames)
    contributions = list(csvfile);

    presentation = 'poster'
    if args.list.find('lbd') > 0:
        presentation = 'lbd'


    # List workspace members
    try:
        response = client.users_list()
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    users = response["members"]
    print(len(users))
    # for u in users: 
    #     email = ''
    #     if 'email' in u['profile']:
    #         email = u['profile']['email']
    #         #u['real_name'],
    #     print(u['name'],u['profile']['real_name'],u['profile']['real_name_normalized'],email)
    # u['is_bot']


    # List channels
    try:
        response = client.conversations_list(limit=200)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    # print(response)
    # print(response['ok'])
    # print(response['response_metadata']['next_cursor']) 
    # print(response['channels'])
    presentations = [c for c in response['channels'] if c['name'].find(presentation) == 0]
    
    # Check for channel info in csv
    for channel_field in ['channel_name','channel_url']:
        if not channel_field in fieldnames:
            print('Create '+channel_field)
            fieldnames.append(channel_field)

    with sessions.Session() as session:

        for contribution in contributions:

            # print(contribution)
            for channel_field in ['channel_name','channel_url']:
                if not channel_field in contribution:
                    contribution[channel_field]=''
            # print(contribution)
            # print(contribution["primary_author"])

            primary_author_names = contribution["primary_author"].split(" ")
            primary_author_name = primary_author_names[len(primary_author_names)-1].lower()
            if presentation == 'lbd':
                channel_name = presentation + "-" + contribution["session"] + "-" + contribution["uid"] + "-" + primary_author_name
            else:
                channel_name = presentation + "-" + contribution["uid"] + "-" + primary_author_name
            # print(channel_name,contribution["channel_name"])
            contribution['channel_name']=channel_name

            channel_id = ''
            if contribution['channel_url'] == '':
                print('Creating channel')
                try:
                    response = client.conversations_create(
                        name=channel_name,
                        is_private=False
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                # print(response)
                channel_id = response["channel"]["id"]
                channel_url = channels_url + channel_id
                contribution['channel_url']=channel_url
            else:
                channel_url = contribution['channel_url']
                channel_id = channel_url.replace(channels_url,'')
                # print(channel_id)

            # Check if channel exists
            channel = [c for c in presentations if c['id'] == channel_id ]

            # Find authors
            authors = []
            def find_author(u,names):
                found = True
                for name in names:
                    name = name.replace('.','')
                    # print(u['profile']['real_name'],name)
                    if len(name) > 1:
                        found = found and u['profile']['real_name'].lower().find(name.lower()) > -1
                return found
    
            contributors = contribution["authors"].split('|');
            for contributor in contributors:
                names = contributor.split(' ')
                # user = [u for u in users if u['profile']['real_name'].lower().find(names[0].lower()) > -1 and u['profile']['real_name'].lower().find(names[1].lower()) > -1]
                user = [u for u in users if find_author(u,names) == True]
                # print(len(user))
                if len(user) != 1:
                    first_initial = names.copy()
                    first_initial[0] = first_initial[0][0]
                    user = [u for u in users if find_author(u,first_initial) == True]

                # print(len(user))
                if len(user) == 1:
                    # print(user)
                    authors.append("<@"+user[0]['id']+">")
                else:
                    authors.append(contributor)

            # Define topic
            channel_topic = ''
            channel_topic += "<https://program.ismir2020.net/";
            if presentation == 'lbd':
                channel_topic += presentation + "_" + contribution["uid"]
            else:
                channel_topic += presentation + "_" + contribution["uid"]
            channel_topic += ".html>"
            channel_topic += " \"" + contribution["title"] + " \""    
            channel_topic += " by " + ", ".join(authors)
            # print(channel_topic)

            # Change topic
            topic = ''
            if len(channel) == 1:
                topic = channel[0]['topic']['value']
            # print(topic,channel_topic)
            if topic != channel_topic: 
                try:
                    response = client.conversations_setTopic(
                        channel=channel_id,
                        topic=channel_topic
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

                # Get channel messages
                try:
                    response = client.search_messages(
                        # query="in:"+channel_name,
                        query="in:"+channel_name+" set the channel topic",
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                # print("response",response)

                messages = response['messages']['matches']

                # Remove channel change topic messages
                for m in messages:
                    if m["channel"]["id"] == channel_id:
                        try:
                            response = client.chat_delete(
                                channel=channel_id,
                                ts=m["ts"]
                            )
                        except SlackApiError as e:
                            # You will get a SlackApiError if "ok" is False
                            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                        #print("response",response)


    # print("Saving CSV")
    # res = csv.DictWriter(open(args.list, 'w', newline=''),fieldnames=fieldnames)
    # res.writeheader()
    # res.writerows(contributions)

