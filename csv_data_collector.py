import csv
import random

class CSVDataCollector():

    '''
    Use add_data to add data to the csv\n
    Use create_csv to create a new file using added data\n
    Distance is pixels from the button\n
    Size is the diameter of the button in pixels\n
    Direction is either left or right\n
    Time is the time in ms it took to click the button\n
    Distance traveled is the amount of pixels traveled before clicking the button\n
    Errors are any extra clicks not on the correct button
    '''

    def __init__(self):
        self.data = [['Distance','Size','Direction','Time','Distance Traveled','Misclick']]

    def add_data(self,distance,size,direction,time,distanceTraveled,misclick):
        self.data.append([distance,size,direction,time,distanceTraveled,misclick])

    def create_csv(self,fileName):
        fileCreated = False
        fileNumber = random.randint(1, 1000000) 
        while fileCreated == False:
            try:
                with open(f"{fileNumber} - {fileName}.csv",'x',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.data)
                    fileCreated = True
            except FileExistsError:
                fileNumber += 1