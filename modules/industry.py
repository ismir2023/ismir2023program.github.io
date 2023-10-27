import pandas as pd
import copy
import time


# Defining the class that exposes the methods related to papaers.
class Industry:
    """
    This method takes the config data loaded and the papers csv file.
    """
    def __init__(self, industryCsvFile, registrationCsvFile, useDummyValues):
        print("Initialising lbds")
        self.industryCsvFile = industryCsvFile
        self.useDummyValues = useDummyValues
        self.registrationCsvFile = registrationCsvFile

    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.industryCsvFile is None):
            raise Exception("self.industryCsvFile passed in contructor is null")
        
        # Reading the papers data.
        csv_data = pd.read_csv(self.industryCsvFile)

        print(csv_data)

        slack_channel_column = "channel_name"
        catrgory_column_name = "session"
        
        print("########### Now creating slack channels ##########")
        slackUtils.createPublicSlackChannels(slackUtils.client, self.industryCsvFile, slack_channel_column)

        # Adding the channel link to the file.
        slackUtils.addChannelLinksToCSV(slackUtils.client, self.industryCsvFile, slack_channel_column)

        user_data = {}
        author_emails_column = "registered_emails"
        # Creating data to add authors to the respective channel for lbds.
        for index, row in csv_data.iterrows():
            if(self.useDummyValues):
                user_data[row[slack_channel_column]] = ["swapnilgupta.iiith@gmail.com", "sharathadavanne@gmail.com"]
            else:
                #print("Author email is: ", row[author_emails_column])
                user_data[row[slack_channel_column]] = list(map(str.strip, str(row[author_emails_column]).split(",")))
        
        print(user_data)

        # Now sending emails.
        for channel, emails in user_data.items():
            for email in emails:
                print("Adding user ", email, " to channel ", channel)
                slackUtils.inviteUserToChannel(slackUtils.client, email, channel)
