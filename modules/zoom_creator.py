import pandas as pd

# Defining the class that exposes the folliwing methods.
class ZoomCreator:
    """
    This method takes the path for the zoom file to be 
    """
    def __init__(self, eventsCsvFile):
        self.eventsCsvFile = eventsCsvFile

    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupZoomCalls(self, zoomUtils):
        if(self.eventsCsvFile is None):
            raise Exception("self.tutorialsCsvFile passed in contructor is null")

        # Loading the Zoom file.
        csv_data = pd.read_csv(self.eventsCsvFile)

        # Remove the rows with category as Tutorials, Lunch.
        # Tutorials would be created manually and for Lunch we dont need Zoom calls.
        final_data = csv_data[csv_data.category != "Tutorials"]
        final_data = final_data[final_data.category != "Lunch"]
        
        print("## Number of items to create zoom link for: ", len(final_data.index))
        print("### Final data: ", final_data[["uid", "title", "category"]])

        final_data.to_csv("zoom-details.csv")

        zoomUtils.createZoomLinksIfNeeded("zoom-details.csv", "title", "zoom_link", "uid")