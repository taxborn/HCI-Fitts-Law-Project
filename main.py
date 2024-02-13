import wx
import math
import time
import mouse
import webbrowser
import itertools
from random import shuffle
from screeninfo import get_monitors
from csv_data_collector import CSVDataCollector
from completed_page import CompletedPage

BACKGROUND_COLOR = wx.Colour(49, 50, 68)
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
        self.panel.SetBackgroundColour(BACKGROUND_COLOR)
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
        webbrowser.open(
            "https://github.com/taxborn/HCI-Fitts-Law-Project/blob/main/Fitts'%20Law%20Informed%20Consent.pdf"
        )
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
        self.initialize_ui()
        self.csv = CSVDataCollector()
        self.button_data = generate_button_types()
        self.current_button_index = 0
        self.current_errors = 0
        self.create_next_button()
        self.ShowFullScreen(True)
        self.time = time.time()
        self.fullTime = time.time()
        vbox = wx.BoxSizer(wx.VERTICAL)
        message = wx.StaticText(
            self.panel,
            -1,
            f"{self.current_button_index}/320",
            style=wx.ALIGN_TOP,
        )
        message.SetForegroundColour((255, 255, 255))
        font = wx.Font(
            20,
            family=wx.FONTFAMILY_MODERN,
            style=0,
            weight=90,
            underline=False,
            faceName="",
            encoding=wx.FONTENCODING_DEFAULT,
        )
        message.SetFont(font)
        vbox.Add(message, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 90)

    def initialize_ui(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BACKGROUND_COLOR)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_panel_click)

    @property
    def current_button_data(self):
        """Returns the current button's size, distance, and side as a tuple."""
        return self.button_data[self.current_button_index]

    def update_mouse_position(self):
        # Set the mouse position to the center of the screen
        mouse.move(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

    def create_button(self, size, distance, side):
        """Creates a button based on specified size, distance, and side."""
        self.time = time.time()
        self.button = wx.Button(self.panel, size=wx.Size(size, size))

        # Calculate where it should be on the screen
        self.pos_x = int(side * distance + SCREEN_SIZE[0] // 2)
        # For the y-position, we need to subtract by half the size to actually center on the screen
        self.pos_y = int(SCREEN_SIZE[1] // 2 - (size // 2))
        self.button.SetPosition((self.pos_x, self.pos_y))

    def create_next_button(self):
        self.current_errors = 0
        # End of the experiment check
        if self.current_button_index >= len(self.button_data) - 1:
            self.csv.save("Fitts Law Data")
            end = CompletedPage(None, "CompletedPage", time.time() - self.time)
            end.Show()
            self.Close()
            return

        self.update_mouse_position()
        self.create_button(*self.current_button_data)
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

    def on_button_click(self, event):
        """Handles button click events, records data, and prepares the next button."""
        size, distance, side = self.current_button_data
        elapsed_time = time.time() - self.time
        mouse_pos = mouse.get_position()
        distance_traveled = math.sqrt(
            (mouse_pos[0] - self.pos_x) ** 2 + (mouse_pos[1] - self.pos_y) ** 2
        )

        # Add the data to the CSV
        self.csv.add_data(
            distance, size, side, elapsed_time, distance_traveled, self.current_errors
        )
        # Destroy the button
        event.GetEventObject().Destroy()
        # Increment the index
        self.current_button_index += 1
        vbox = wx.BoxSizer(wx.VERTICAL)
        message = wx.StaticText(
            self.panel,
            -1,
            f"{self.current_button_index}/320",
            style=wx.ALIGN_TOP,
        )
        message.SetForegroundColour((255, 255, 255))
        font = wx.Font(
            20,
            family=wx.FONTFAMILY_MODERN,
            style=0,
            weight=90,
            underline=False,
            faceName="",
            encoding=wx.FONTENCODING_DEFAULT,
        )
        message.SetFont(font)
        vbox.Add(message, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 90)
        # Create the next button
        self.create_next_button()

    def on_panel_click(self, event):
        """Increments the error count when the panel is clicked outside a button."""
        self.current_errors += 1


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
