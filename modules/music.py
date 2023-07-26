import pandas as pd
import copy
import time


# Defining the class that exposes the methods related to papaers.
class Music:
    """
    This method takes the config data loaded and the music csv file.
    """
    def __init__(self, musicCsvFile, useDummyValues):
        print("Initialising music")
        self.musicCsvFile = musicCsvFile
        self.useDummyValues = useDummyValues

    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.musicCsvFile is None):
            raise Exception("self.musicCsvFile passed in contructor is null")
        
        # Reading the papers data.
        csv_data = pd.read_csv(self.musicCsvFile)

        print(csv_data)

        slack_channel_column = "channel_name"
        
        print("########### Now creating slack channels ##########")
        slackUtils.createPublicSlackChannels(slackUtils.client, self.musicCsvFile, slack_channel_column)

        # Adding the channel link to the file.
        slackUtils.addChannelLinksToCSV(slackUtils.client, self.musicCsvFile, slack_channel_column)

        user_data = {}
        author_emails_column = "author_emails"
        # Creating data to add authors to the respective channel for lbds.
        for index, row in csv_data.iterrows():
            if(self.useDummyValues):
               user_data[row[slack_channel_column]] = ["swapnilgupta.iiith@gmail.com", "sharathadavanne@gmail.com"]
            else:
               user_data[row[slack_channel_column]] = list(map(str.strip, row[author_emails_column].replace("|", ",").split(",")))    
    
        
        print(user_data)

        # Now sending emails.
        for channel, emails in user_data.items():
            for email in emails:
                print("Adding user ", email, " to channel ", channel)
                slackUtils.inviteUserToChannel(slackUtils.client, email, channel)
