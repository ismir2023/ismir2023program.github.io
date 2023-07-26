import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
accountCreds = {
    "accountId": os.environ['accountId'],
    "clientId": os.environ['clientId'],
    "clientSecret": os.environ['clientSecret']
}
accessToken = None
tokenExpireTime = None


def getAccessToken(accountCreds):
    """
    returns access token used in Zoom API calls
    """
    getTokenUrl = (f"https://zoom.us/oauth/token"
        + f"?grant_type=account_credentials&account_id={accountCreds['accountId']}"
    )
    resp = requests.post(
        getTokenUrl,
        auth=(accountCreds['clientId'], accountCreds['clientSecret'])
    )
    respJson = resp.json()
    # token expire time in seconds since epoch
    tokenExpireTime = int(respJson['expires_in']) - 10 + int(time.time())
    return (
        respJson['access_token'],
        tokenExpireTime
    )



def checkToken():
    if accessToken is None:
        return getAccessToken(accountCreds)
    if(time.time() < tokenExpireTime):
        return (accessToken, tokenExpireTime)
    else:
        return getAccessToken(accountCreds)

def getListOfMeetings():
    accessToken, tokenExpireTime = checkToken()
    meetingList = []
    apiEndpointUrl = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    queryData = {
        "type": "scheduled",
        "page_size": 300
    }
    resp = requests.get(
        apiEndpointUrl,
        params=queryData,
        headers=headers
    )
    respJson = resp.json()

    for meeting in respJson['meetings']:
        meetingList.append((meeting['id'], meeting['topic']))
    i=1
    while(respJson['next_page_token'] != ''):
        queryData = {
            "type": "scheduled",
            "page_size": 300,
            "next_page_token": respJson['next_page_token'],
            "page_number": i
        }
        resp = requests.get(
            apiEndpointUrl,
            params=queryData,
            headers=headers
        )
        respJson = resp.json()
        for meeting in respJson['meetings']:
            meetingList.append((meeting['id'], meeting['topic']))
        i += 1
    return meetingList

def doesMeetingExist(accessToken, tokenExpireTime, accountCreds, key_type, key_val):
    """
    key_type: "topic" or "id"
    key_val: meeting topic (str) or meeting id (int)
    """
    accessToken, tokenExpireTime, meetingList = getListOfMeetings(
        accessToken,
        tokenExpireTime,
        accountCreds
    )
    # meetingList is a list of (id, topic) tuples
    if key_type == "topic":
        return (
            accessToken,
            tokenExpireTime,
            (key_val in [meeting[1] for meeting in meetingList])
        )
    elif key_type == "id":
        return (
            accessToken,
            tokenExpireTime,
            (key_val in [meeting[0] for meeting in meetingList])
        )
    else:
        print(f"Invalid key_type ({key_type}) given to doesMeetingExist()")

def createMeeting(meetingTopic, startTime, duration):
    accessToken, tokenExpireTime = checkToken()
    apiEndpointUrl = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    meetingDetails = {
        "topic": meetingTopic,
        "type": 2,  # scheduled meeting
        "start_time": startTime, # "2022-10-23T01: 15: 00",
        # "duration": duration, # "45", # in minutes
        "timezone": "Asia/Calcutta",
        "settings": {
            "waiting_room": False,
            "join_before_host": True,
            "jbh_time": 0 # anytime before host
        }
    }
    resp = requests.post(
        apiEndpointUrl,
        data=json.dumps(meetingDetails),
        headers=headers
    )
    return resp.json()

def deleteMeeting(accessToken, tokenExpireTime, accountCreds, meetingId):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    apiEndpointUrl = f"https://api.zoom.us/v2/meetings/{meetingId}"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    resp = requests.delete(
        apiEndpointUrl,
        headers=headers
    )
    return (accessToken, tokenExpireTime)

def createZoomLinksIfNeeded(csvFilename, topicColumnId, zoomColumnId, indexColumnId):
    csvData = pd.read_csv(csvFilename, index_col=indexColumnId)
    existingMeetings = getListOfMeetings()
    existingMeetingTopics = [meeting[1] for meeting in existingMeetings]

    for index, row in csvData.iterrows():
        if row[topicColumnId] not in existingMeetingTopics:
            respJson = createMeeting(
                row[topicColumnId],
                row['start_date'] + 'T' + row['start_time'],
                "",
            )
            existingMeetings.append((respJson['id'], respJson['topic']))
            existingMeetingTopics.append(respJson['topic'])
            csvData.loc[index, zoomColumnId] = respJson['join_url']
    csvData.to_csv(csvFilename)

def createWebinar(accessToken, tokenExpireTime, accountCreds, topic, startTime, duration):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    apiEndpointUrl = "https://api.zoom.us/v2/users/me/webinars"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    webinarDetails = {
        "topic": topic,
        "type": 5, # scheduled webinar
        "start_time": startTime, # "2022-10-23T01: 15: 00",
        "duration": duration, # "45", # in minutes
        "timezone": "Asia/Calcutta",
    }
    resp = requests.post(
        apiEndpointUrl,
        data=json.dumps(webinarDetails),
        headers=headers
    )
    return accessToken, tokenExpireTime, resp.json()

def addPanelistsToWebinar(accessToken, tokenExpireTime, accountCreds, webinarId, panelistList):
    """
    panelists: list of tuples (email, name)
    """
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    apiEndpointUrl = f"https://api.zoom.us/v2/users/me/webinars/{webinarId}/panelists"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    panelists = [
        {
            "email": email,
            "name": name
        }
        for (email, name) in panelistList
    ]
    resp = requests.post(
        apiEndpointUrl,
        data=json.dumps(panelists),
        headers=headers
    )
    return accessToken, tokenExpireTime, resp.json()

def getListOfPanelistsInWebinar(accessToken, tokenExpireTime, accountCreds, webinarId):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    panelistList = []
    apiEndpointUrl = f"https://api.zoom.us/v2/webinars/{webinarId}/panelists"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    resp = requests.get(
        apiEndpointUrl,
        headers=headers
    )
    respJson = resp.json()
    for panelist in respJson['panelists']:
        panelistList.append(
            (
                panelist['id'],
                panelist['name'],
                panelist['email'],
                panelist['join_url']
            )
        )
    return accessToken, tokenExpireTime, panelistList

def getListOfWebinars(accessToken, tokenExpireTime, accountCreds):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    webinarList = []
    apiEndpointUrl = "https://api.zoom.us/v2/users/me/webinars"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    queryData = {
        "type": "scheduled",
        "page_size": 300
    }
    resp = requests.get(
        apiEndpointUrl,
        params=queryData,
        headers=headers
    )
    respJson = resp.json()

    for webinar in respJson['webinars']:
        webinarList.append((webinar['id'], webinar['topic']))

    while(respJson['next_page_token'] != ''):
        queryData = {
            "type": "scheduled",
            "page_size": 300,
            "next_page_token": respJson['next_page_token']
        }
        resp = requests.get(
            apiEndpointUrl,
            params=queryData,
            headers=headers
        )
        respJson = resp.json()
        for webinar in respJson['webinars']:
            webinarList.append((webinar['id'], webinar['topic']))
    return accessToken, tokenExpireTime, webinarList

def deleteWebinar(accessToken, tokenExpireTime, accountCreds, webinarId):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    apiEndpointUrl = f"https://api.zoom.us/v2/webinars/{webinarId}"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    resp = requests.delete(
        apiEndpointUrl,
        headers=headers
    )
    return accessToken, tokenExpireTime

def deletePanelistFromWebinar(accessToken, tokenExpireTime, accountCreds, webinarId, panelistId):
    accessToken, tokenExpireTime = checkToken(accessToken, tokenExpireTime, accountCreds)
    apiEndpointUrl = f"https://api.zoom.us/v2/webinars/{webinarId}/panelists/{panelistId}"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "content-type": "application/json"
    }
    resp = requests.delete(
        apiEndpointUrl,
        headers=headers
    )
    return accessToken, tokenExpireTime

######################################################################
########################## testing meetings ##########################
######################################################################
# import pandas as pd
#
# # df = pd.read_csv("test_csv.csv", index_col='uid')
# # accessToken, tokenExpireTime = getAccessToken(accountCreds)
# accessToken = None
# tokenExpireTime = None
#
# print(getListOfMeetings())
# createZoomLinksIfNeeded(
#     "test_csv.csv",
#     "topic",
#     "zoom_link",
#     "uid"
# )
# # print(df)
#
# # time.sleep(3650) # 3650 seconds
#
# print(getListOfMeetings())

# print((accessToken, tokenExpireTime, meetingList))
#
# sampleMeeting = meetingList[0]
# accessToken, tokenExpireTime, sampleMeetingExistsTopic = doesMeetingExist(
#     accessToken,
#     tokenExpireTime,
#     accountCreds,
#     "topic",
#     sampleMeeting[1]
# )
# accessToken, tokenExpireTime, sampleMeetingExistsId = doesMeetingExist(
#     accessToken,
#     tokenExpireTime,
#     accountCreds,
#     "id",
#     sampleMeeting[0]
# )
#
# print(meetingList)
# print(f"Does {sampleMeeting} exist?")
# print(f"Check by topic: {sampleMeetingExistsTopic}")
# print(f"Check by id: {sampleMeetingExistsId}")
#
# print(f"\nNow deleting ({sampleMeeting})\n")
#
# accessToken, tokenExpireTime = deleteMeeting(
#     accessToken,
#     tokenExpireTime,
#     accountCreds,
#     sampleMeeting[0]
# )
#
# accessToken, tokenExpireTime, sampleMeetingExistsTopic = doesMeetingExist(
#     accessToken,
#     tokenExpireTime,
#     accountCreds,
#     "topic",
#     sampleMeeting[1]
# )
# accessToken, tokenExpireTime, sampleMeetingExistsId = doesMeetingExist(
#     accessToken,
#     tokenExpireTime,
#     accountCreds,
#     "id",
#     sampleMeeting[0]
# )
#
# print("check by id:", sampleMeetingExistsId)
# print("check by topic:", sampleMeetingExistsTopic)