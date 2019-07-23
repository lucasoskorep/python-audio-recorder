from Recorder import Recorder


class ButtonRecorder(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.rec = Recorder(channels=2)

    def set_file_name(self, filename):
        self.filename = filename

    def on_released(self):
        if (self.filename != None):
            self.recfile.stop_recording()
            self.recfile.close()

    def on_pressed(self):
        if (self.filename != None):
            self.recfile = self.rec.open(self.filename, 'wb')
            self.recfile.start_recording()
