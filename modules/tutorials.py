import pandas as pd
import copy
import os
import numpy as np


MORNING_TUTORIAL_COL = "Select the morning session tutorial you wish to attend"
AFTERNOON_TUTORIAL_COL = "Select the afternoon session tutorial you wish to attend"
ATTENDEE_EMAIL = "Attendee Email"

# Defining the class that exposes the folliwing methods.
class Tutorials:
    """
    This method takes the config data loaded and the tutorials csv file.
    """
    def __init__(self, eventsCsvFile, townscriptCsvFile, useDummyValues):
        self.eventsCsvFile = eventsCsvFile
        self.townscriptCsvFile = townscriptCsvFile
        self.useDummyValues = useDummyValues

    """
    This method inputs the slack utils, and uses it to create the slack channels.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.eventsCsvFile is None):
            raise Exception("self.eventsCsvFile passed in contructor is null")
        
        if(self.townscriptCsvFile is None):
            raise Exception("self.townscriptCsvFile passed in contructor is null")
        
        # Loading events data and creating tutorials file from there.
        # Loading the Zoom file.
        csv_data = pd.read_csv(self.eventsCsvFile)

        # Filter only for tutorials.
        csv_data = csv_data[csv_data.category == "Tutorials"]
        print("### Tutorials are: ", csv_data)

        tutorials_file_name = "tutorials_for_slack.csv"

        csv_data.to_csv(tutorials_file_name)
        # Creating slack channels ...
        print("Trying to create channels if already not created")
        slackUtils.createPrivateSlackChannels(slackUtils.client, tutorials_file_name, "slack_channel")

        # Adding the channel link to the file.
        slackUtils.addChannelLinksToCSV(slackUtils.client, tutorials_file_name, "slack_channel")
        

        print("############################################") 
        print("#########Creating of channels done##########") 
        print("############################################") 

        # Updating the description of the slack channels.
        # TODO - Update the title instead.
        # print("Starting to update the description now")
        # csv_data = pd.read_csv(self.tutorialsCsvFile)
        #for index, entry in csv_data.iterrows():
            #targetChannel = entry["slack_channel"]
            #targetDesc = entry["description"] # TODO -- Add the zoom call link here
            #print("Updating the description for ", targetChannel, " with desc ", targetDesc)
            # TODO - Remove this.. this wont work.
            #slackUtils.updateDescription(slackUtils.client, targetChannel, targetDesc)

        # Adding users to respective slack channels.
        print("Starting to add users to respective slack channels")
        # titles is of format {<title>: (<channel_id>, [... list of email ids])}
        titles = {}

        # Reading all the titles
        for index, entry in csv_data.iterrows():
            titles[entry["title"].lower()] = (entry["slack_channel"], [])

        # Creating a lower case list.
        # titles_lower_case = {title.lower(): title, val in titles.items()} 
        
        # Cleaning the data bit. Removing the trailing quotes and equal to.
        townscript_data = pd.read_csv(self.townscriptCsvFile)
        
        titles_not_found = []
        # Iterating over each row for the townscript data.
        for index, entry in townscript_data.iterrows():
            # Checking for 
            if(getCleanTitle(entry[MORNING_TUTORIAL_COL]) in titles):
                # Appending email to the tutorial list.
                titles[getCleanTitle(entry[MORNING_TUTORIAL_COL])][1].append(entry[ATTENDEE_EMAIL])
            if(getCleanTitle(entry[AFTERNOON_TUTORIAL_COL]) in titles):
                titles[getCleanTitle(entry[AFTERNOON_TUTORIAL_COL])][1].append(entry[ATTENDEE_EMAIL])
            else:
                titles_not_found.append(getCleanTitle(entry[AFTERNOON_TUTORIAL_COL]))

        print("Tutorials and attendes", titles)

        print("############################################") 
        print("#########Titles not found#######") 
        print("############################################")
        print("titles_not_found", titles_not_found)

        print("Starting to send out invites")

        # Creating a deep copy.
        titles_to_be_used = copy.deepcopy(titles)

        # If we have to use dummy values, then we just send invites to dummy values.
        if(self.useDummyValues):
            for key in titles_to_be_used.keys():
                titles_to_be_used[key] = (titles_to_be_used[key][0], ["swapnilgupta.iiith@gmail.com", "sharathadavanne@gmail.com"])
        
        print("######## The final data for emails is", titles_to_be_used)

        # Finally sending the invite emails.
        for channel_email_tuple in titles_to_be_used.values():
            for email in channel_email_tuple[1]:
                print("Adding user ", email, " to channel ", channel_email_tuple[0])
                slackUtils.inviteUserToChannel(slackUtils.client, email, channel_email_tuple[0].replace("#", ''))

        # Adding the slack channel URL to the original file.
        csv_data = pd.read_csv(self.eventsCsvFile)
        tutorials_data = pd.read_csv(tutorials_file_name)
        
        for i, row_with_url in tutorials_data.iterrows():
            for j, row_wo_url in csv_data.iterrows():
                if(row_with_url["slack_channel"] == row_wo_url["slack_channel"]):
                    print("Adding URL ", row_with_url["channel_url"], " to ", row_with_url["title"])
                    csv_data.loc[j, "channel_url"] = row_with_url["channel_url"]
        
        # print("Data after copying channel_urls: ", csv_data)

        # Owerwriting the file.
        csv_data.to_csv(self.eventsCsvFile)

        # Removing the temporary file since the work is done.
        os.remove(tutorials_file_name)


def getCleanTitle(incoming):
    return str(incoming).replace('"', '').replace('=', '').lower()
