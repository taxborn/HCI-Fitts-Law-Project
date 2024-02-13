import wx
import math
import time
import mouse
import webbrowser
import itertools
from random import shuffle
from screeninfo import get_monitors
from csv_data_collector import CSVDataCollector

SCREEN_SIZE = get_monitors()[0].width, get_monitors()[0].height
BUTTON_SIZES = [64, 128, 196, 256]
BUTTON_DISTANCES = [300, 400, 500, 600]
BUTTON_SIDES = [-1, 1]  # -1 = left, 1 = right
TRAILS_PER_CONFIGURATION = 10


class InformedConsentFrame(wx.Frame):
    def __init__(self, parent, title):
        super(InformedConsentFrame, self).__init__(
            parent,
            title=title,
            size=(int(SCREEN_SIZE[0] * 0.75), int(SCREEN_SIZE[1] * 0.75)),
        )
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(49, 50, 68))
        self.Centre()
        self.initialize_ui()

    def initialize_ui(self):
        # vertical boxsizer which contains all the buttons
        vbox = wx.BoxSizer(wx.VERTICAL)

        # use to size the start button so that is is always in the center of the screen
        vbox.Add(-1, 1, wx.EXPAND)

        # Button to open the consent form PDF
        self.consent_form_button = wx.Button(
            self.panel, label="Open Consent Form", size=(150, 50)
        )
        self.consent_form_button.Bind(wx.EVT_BUTTON, self.on_open_consent_form)
        vbox.Add(
            self.consent_form_button,
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,
            border=10,
        )

        # Horizontal box sizer for 'I Agree' and 'No, I do not wish to continue' buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 'I Agree' button (hidden initially)
        self.agree_button = wx.Button(self.panel, label="I Agree", size=(150, 50))
        self.agree_button.Bind(wx.EVT_BUTTON, self.on_agree)
        hbox.Add(self.agree_button, flag=wx.RIGHT, border=10)
        self.agree_button.Hide()

        # 'No, I do not wish to continue' button (hidden initially)
        self.disagree_button = wx.Button(
            self.panel, label="I do not wish to continue", size=(150, 50)
        )
        self.disagree_button.Bind(wx.EVT_BUTTON, self.on_disagree)
        hbox.Add(self.disagree_button)
        self.disagree_button.Hide()

        vbox.Add(hbox, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)

        # 'Start' button (hidden initially, larger size, centered)
        self.start_button = wx.Button(self.panel, label="Start", size=(200, 100))
        self.start_button.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        vbox.Add(self.start_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)
        self.start_button.Hide()

        # Add another stretchable space after the Start button (with a proportion of 1)
        vbox.Add(-1, 1, wx.EXPAND)

        self.panel.SetSizer(vbox)

    def on_open_consent_form(self, event):
        webbrowser.open("Sample Fitts' Law Informed Consent.pdf")
        self.agree_button.Show()
        self.disagree_button.Show()
        self.panel.Layout()

    def on_agree(self, event):
        wx.MessageBox(
            "Thanks for participating. We can start the experiment now.",
            "Consent Acknowledged",
            wx.OK | wx.ICON_INFORMATION,
        )
        self.consent_form_button.Hide()
        self.agree_button.Hide()
        self.disagree_button.Hide()
        self.start_button.Show()
        self.panel.Layout()

    def on_disagree(self, event):
        wx.MessageBox(
            "We understand your choice.",
            "Consent Not Given",
            wx.OK | wx.ICON_INFORMATION,
        )
        self.Close()

    def on_start(self, event):
        self.start_button.Hide()
        exp = Experiment(None, "Experiment")
        exp.Show()
        self.Close()


class Experiment(wx.Frame):
    def __init__(self, parent, title):
        super(Experiment, self).__init__(
            parent,
            title=title,
            size=(int(SCREEN_SIZE[0] * 0.75), int(SCREEN_SIZE[1] * 0.75)),
        )
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(49, 50, 68))
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_panel_click)

        self.button_data = generate_button_types()
        self.current_button_index = 0
        self.create_button()
        self.ShowFullScreen(True)
        self.time = time.time()

        self.csv = CSVDataCollector()

    def create_button(self):
        # End of the experiment check
        if self.current_button_index >= len(self.button_data) - 1:
            self.csv.save("Fitts Law Data")
            self.Close()

        # update the time
        self.time = time.time()
        # Set the mouse position
        mouse.move(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        # Destruct the current button data
        size, distance, side = self.button_data[self.current_button_index]
        # Create the button
        self.button = wx.Button(self.panel, label=f" ", size=wx.Size(size, size))
        # Calculate where it should be on the screen
        self.pos_x = int(side * distance + SCREEN_SIZE[0] // 2)
        # For the y-position, we need to subtract by half the size to actually center on the screen
        self.pos_y = int(SCREEN_SIZE[1] // 2 - (size // 2))
        self.button.SetPosition((self.pos_x, self.pos_y))

        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

    def on_button_click(self, event):
        # button data
        size, distance, side = self.button_data[self.current_button_index]
        elapsed = time.time() - self.time
        mouse_pos = mouse.get_position()
        traveled = math.sqrt(
            (mouse_pos[0] - self.pos_x) ** 2 + (mouse_pos[1] - self.pos_y) ** 2
        )

        # Destroy the button
        event.GetEventObject().Destroy()
        # Add the data to the CSV
        self.csv.add_data(distance, size, side, elapsed, traveled, 0)
        # Increment the index
        self.current_button_index += 1
        # Create the next button
        self.create_button()

    def on_panel_click(self, event):
        # This only runs when we click outside of the box.
        size, distance, side = self.button_data[self.current_button_index]
        elapsed = time.time() - self.time
        mouse_pos = mouse.get_position()
        traveled = math.sqrt(
            (mouse_pos[0] - self.pos_x) ** 2 + (mouse_pos[1] - self.pos_y) ** 2
        )

        # reset the time
        self.time = time.time()
        self.csv.add_data(distance, size, side, elapsed, traveled, 1)


def generate_button_types() -> list[tuple[int, int, int]]:
    # Generate all possible combinations of size, distance, and direction for buttons
    all_combinations = list(
        itertools.product(BUTTON_SIZES, BUTTON_DISTANCES, BUTTON_SIDES)
    )
    # Replicate the combinations list 10 times to create a larger pool of options
    repeated_combinations = all_combinations * TRAILS_PER_CONFIGURATION
    # Shuffle the list to randomize the order of options
    shuffle(repeated_combinations)

    return repeated_combinations


if __name__ == "__main__":
    app = wx.App(False)
    ic = InformedConsentFrame(None, "Fitt's Law Project")
    ic.Show()
    app.MainLoop()
