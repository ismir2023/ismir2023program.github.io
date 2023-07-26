import pandas as pd
import copy
import time


# Defining the class that exposes the methods related to papaers.
class Lbds:
    """
    This method takes the config data loaded and the papers csv file.
    """
    def __init__(self, lbdsCsvFile, useDummyValues):
        print("Initialising lbds")
        self.lbdsCsvFile = lbdsCsvFile
        self.useDummyValues = useDummyValues

    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.lbdsCsvFile is None):
            raise Exception("self.lbdsCsvFile passed in contructor is null")
        
        # Reading the papers data.
        csv_data = pd.read_csv(self.lbdsCsvFile)

        print(csv_data)
        slack_channel_column = "channel_name"

        # Preparing the slack channel name.
        for index, row in csv_data.iterrows():
            names_array = row["primary_author"].lower().strip().split()
            names_array.reverse()
            if(row["session"].strip() == "Physical"):
                csv_data.loc[index, slack_channel_column] = "lp-" + str(row["position"]) + "-" + str(names_array[0])
            else:
                csv_data.loc[index, slack_channel_column] = "lv-" + str(row["position"]) + "-" + str(names_array[0])

        # Overwriting the file.
        csv_data.to_csv(self.lbdsCsvFile)
        
        print("########### Now creating slack channels ##########")
        slackUtils.createPublicSlackChannels(slackUtils.client, self.lbdsCsvFile, slack_channel_column)

        # Adding the channel link to the file.
        slackUtils.addChannelLinksToCSV(slackUtils.client, self.lbdsCsvFile, slack_channel_column)

        user_data = {}
        author_emails_column = "author_emails"
        # Creating data to add authors to the respective channel for lbds.
        for index, row in csv_data.iterrows():
            if(self.useDummyValues):
                user_data[row[slack_channel_column]] = ["swapnilgupta.iiith@gmail.com", "sharathadavanne@gmail.com"]
            else:
                user_data[row[slack_channel_column]] = list(map(str.strip, str(row[author_emails_column]).split(",")))    
        
        print(user_data)

        # Now sending emails.
        for channel, emails in user_data.items():
            for email in emails:
                print("Adding user ", email, " to channel ", channel)
                slackUtils.inviteUserToChannel(slackUtils.client, email, channel)
