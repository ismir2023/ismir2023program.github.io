import pandas as pd
import copy
import time


# Defining the class that exposes the methods related to papaers.
class Papers:
    """
    This method takes the config data loaded and the papers csv file.
    """
    def __init__(self, papersCsvFile, useDummyValues):
        self.papersCsvFile = papersCsvFile
        self.useDummyValues = useDummyValues

    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.papersCsvFile is None):
            raise Exception("self.papersCsvFile passed in contructor is null")
        
        # Reading the papers data.
        csv_data = pd.read_csv(self.papersCsvFile)

        slack_channel_column = "slack_channel"

        csv_data.loc[:, slack_channel_column] = ""

        # Iterating over each row and creating the slack_channel_column
        # Format is P<session_nunmber>-<position>-<author_last_name>.
        for index, row in csv_data.iterrows():
            names_array = row["primary_author"].lower().strip().split()
            names_array.reverse()
            csv_data.loc[index, slack_channel_column] = "p" + str(row["session"]) + "-" + '{:0>2}'.format(row["position"] + 1) + "-" + names_array[0]

        print("Data after adding the slack column channel: ", csv_data)
        # Updating the file with the details to be able to write the slack columns.
        csv_data.to_csv(self.papersCsvFile)
        
        print("########### Now creating slack channels ##########")
        slackUtils.createPublicSlackChannels(slackUtils.client, self.papersCsvFile, slack_channel_column)

        # Adding the channel link to the file.
        slackUtils.addChannelLinksToCSV(slackUtils.client, self.papersCsvFile, slack_channel_column)

        # Adding the authors to the papers channel.
        user_details = {}
        for index, data in csv_data.iterrows():
            print("Row is: ", data)
            user_details[data[slack_channel_column]] = str(data["author_emails"]).replace(" ", "").replace("*", "").split(";")


        if(self.useDummyValues):
            print("Have to use dummy values!!!")
            for key, value in user_details.items():
                user_details[key] = ["swapnilgupta.iiith@gmail.com", "sharathadavanne@gmail.com"]

        # Sending invites to users.
        print("The user details are: ", user_details)

        # Finally sending invites.
        for key, emails in user_details.items():
            for email in emails:
                print("Sending email for ", key, " to ", email)
                slackUtils.inviteUserToChannel(slackUtils.client, email, key)
