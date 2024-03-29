import os
import csv
import random


class CSVDataCollector:

    """
    Use add_data to add data to the csv
    Use save to create a new file using added data
    Distance is pixels from the button
    Size is the diameter of the button in pixels
    Direction is either left or right
    Time is the time in ms it took to click the button
    Distance traveled is the amount of pixels traveled before clicking the button (the diagonal)
    Errors are any extra clicks not on the correct button
    """

    def __init__(self):
        # The header for the CSV
        self.data = [
            ["Distance", "Size", "Direction", "Time", "Distance Traveled", "Errors"]
        ]

    def add_data(self, *args):
        self.data.append([*args])

    def save(self, fileName):
        # Create the data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data", exist_ok=True)

        fileCreated = False
        fileNumber = random.randint(1, 1000000)

        while fileCreated == False:
            try:
                with open(
                    f"data/{fileNumber} - {fileName}.csv", "x", newline=""
                ) as file:
                    writer = csv.writer(file)
                    writer.writerows(self.data)
                    fileCreated = True
            # If for whatever reason the file already exists,
            except FileExistsError:
                fileNumber += 1
