from Recorder import Recorder


class ButtonRecorder(object):
    def __init__(self, filename=None, device = 0):
        self.filename = filename
        self.rec = Recorder(channels=1, device = device)

    def set_device_index(self, index):
        self.rec.set_device(index)

    def set_file_name(self, filename):
        self.filename = filename

    def on_released(self):
        if (self.filename != None):
            self.recfile.stop_recording()
            self.recfile.close()

    def on_pressed(self):
        if (self.filename != None):
            print(self.filename)
            self.recfile = self.rec.open(self.filename, 'wb')
            self.recfile.start_recording()
