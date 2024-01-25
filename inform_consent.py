import wx
import webbrowser

class FittsLawExperiment(wx.Frame):
    def __init__(self, parent, title):
        super(FittsLawExperiment, self).__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.initialize_ui()
        self.Centre()
        self.Show()

    def initialize_ui(self):
        #vertical boxsizer which contains all the buttons
        vbox = wx.BoxSizer(wx.VERTICAL)

        # use to size the start button so that is is always in the center of the screen 
        vbox.Add(-1, 1, wx.EXPAND)

        # Button to open the consent form PDF
        self.consent_form_button = wx.Button(self.panel, label="Open Consent Form", size=(150, 50))
        self.consent_form_button.Bind(wx.EVT_BUTTON, self.on_open_consent_form)
        vbox.Add(self.consent_form_button, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)

        # Horizontal box sizer for 'I Agree' and 'No, I do not wish to continue' buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 'I Agree' button (hidden initially)
        self.agree_button = wx.Button(self.panel, label="I Agree", size=(150, 50))
        self.agree_button.Bind(wx.EVT_BUTTON, self.on_agree)
        hbox.Add(self.agree_button, flag=wx.RIGHT, border=10)
        self.agree_button.Hide()

        # 'No, I do not wish to continue' button (hidden initially)
        self.disagree_button = wx.Button(self.panel, label="I do not wish to continue", size=(150, 50))
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
        consent_form_path = "C:\\Users\\Rania\\Documents\\SpringProject2024\\HCI-Fitts-Law-Project\\Sample Fitts' Law Informed Consent.pdf"
        webbrowser.open(consent_form_path)
        self.agree_button.Show()
        self.disagree_button.Show()
        self.panel.Layout()

    def on_agree(self, event):
        wx.MessageBox("Thanks for participating. We can start the experiment now.", "Consent Acknowledged", wx.OK | wx.ICON_INFORMATION)
        self.consent_form_button.Hide()
        self.agree_button.Hide()
        self.disagree_button.Hide()
        self.start_button.Show()
        self.panel.Layout()

    def on_disagree(self, event):
        wx.MessageBox("We understand your choice.", "Consent Not Given", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_start(self, event):
        print("The experiment has started.")

if __name__ == "__main__":
    app = wx.App(False)
    frame = FittsLawExperiment( None, "Fitt's Law Project")
    app.MainLoop()
