import wx


class CompletedPage(wx.Frame):
    def __init__(self, parent, title, time):
        super(CompletedPage, self).__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.time = time
        self.initialize_ui()
        self.Centre()
        self.Show()

    def initialize_ui(self):
        # the top message
        vbox = wx.BoxSizer(wx.VERTICAL)
        message = wx.StaticText(
            self.panel,
            -1,
            f"Congrats! You have completed the Fitts' Law Experiment.\n "
            f"Thank you for your participation!\n"
            f"Total time: {self.time} seconds.",
            style=wx.ALIGN_CENTER,
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

        # Close Button
        self.close_button = wx.Button(self.panel, label="Close", size=(150, 50))
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close)
        vbox.Add(
            self.close_button, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=100
        )

        self.panel.SetSizer(vbox)

    # runs when the close button is clicked (for now it just closes everything, this can be modified later
    # if we want users to save their data or something)
    def on_close(self, event):
        self.Destroy()


if __name__ == "__main__":
    # Example of using the frame
    app = wx.App(False)
    frame = CompletedPage(None, "Fitt's Law Project")
    app.MainLoop()
