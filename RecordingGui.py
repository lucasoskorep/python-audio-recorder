import uuid
import pyaudio
import os
import errno
import pandas as pd

from ButtonRecorder import ButtonRecorder
from pynput.keyboard import Key, Listener, KeyCode
from tkinter import *

HEIGHT = 2
WIDTH = 35

FONT = ("Courier", 24)

INSTRUCTIONS = "Instructions: " \
               "First select an audio device \n" \
               "Then press start to begin recording \n" \
               "and press stop when you are finished recording.\n" \
               "currently spacebar is set to be the input key, and q quits the recording.\n"

active = False
data_dir = "./data/"
file_base_name = "recording-"

data_filename = "data.csv"
record_key = Key.space
break_key = KeyCode.from_char("q")

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

device = 0

def create_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


create_dir(os.path.join(data_dir, file_base_name))
br = ButtonRecorder(device=device)

gender = None
accent = None
filename = None
age = None
sentence = None
person_name = None
df = pd.read_csv(data_filename)

def on_released(key):
    global active, df, filename, age, sentence, gender, accent
    print('{0} released'.format(
        key))
    if (key == record_key and active):
        active = not active

        br.on_released()
        df = df.append({
            "path":filename,
            "sentence": sentence,
            "age":age,
            "gender":gender,
            "accent":accent,
            "name": person_name
        }, ignore_index=True)
        print(df.tail(10))

def on_pressed(key):
    global active, filename
    if (key == record_key and not active):
        active = not active
        filename = os.path.join(data_dir, file_base_name + str(uuid.uuid4()) + ".wav")
        br.set_file_name(filename)
        br.on_pressed()
    if (key == break_key):
        print("q found")
        raise (Exception("Q pressed"))


class RecordingGui:
    def __init__(self, master, audio_options):
        self.master = master
        self.master.title("Microphone Recorder")

        self.label = Label(master, text=INSTRUCTIONS)
        self.label.pack()

        self.name_input = Entry(master)
        self.name_input.pack()
        self.audio_variable = StringVar(master)
        # self.audio_variable.set(audio_options[0])

        self.audio_list = audio_options
        self.audio_options = OptionMenu(master, self.audio_variable, *audio_options, command=self.select_audio_device)
        self.audio_options.config(height=HEIGHT, width=WIDTH)

        self.accent_variable = StringVar(master)
        self.accent_list = OptionMenu(master, self.accent_variable,
                                      *['us general', 'new york', 'canada', 'england', 'indian', 'hongkong', 'african',
                                        'wales', 'scotland', 'singapore', 'bermuda', 'other', 'australia', 'ireland',
                                        'malaysia', 'philippines', 'newzealand', 'southatlandtic'],
                                      command=self.select_accent)
        self.accent_list.config(height=HEIGHT, width=WIDTH)
        self.accent_list.pack()

        self.gender_variable = StringVar(master)
        self.gender_list = OptionMenu(master, self.gender_variable,
                                      *["male", "female", "other"], command=self.select_gender)
        self.gender_list.config(height=HEIGHT, width=WIDTH)
        self.gender_list.pack()

        self.age_variable = StringVar(master)
        self.age_list = OptionMenu(master, self.age_variable,
                                   *['thirties', 'twenties', 'seventies', 'fourties', 'teens', 'sixties', 'fifties',
                                     'eighties', 'nineties'], command=self.select_age)
        self.age_list.config(height=HEIGHT, width=WIDTH)
        self.age_list.pack()

        self.audio_options.pack()

        self.greet_button = Button(master, text="Start Recording", command=self.start_recording, height=HEIGHT,
                                   width=WIDTH)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit, height=HEIGHT, width=WIDTH)
        self.close_button.pack()

    def enter_name(self, input_val):
        print(input_val)

    def select_accent(self, selected_val):
        print(selected_val)
        global accent
        accent = selected_val

    def select_gender(self, selected_val):
        print(selected_val)
        global gender
        gender = selected_val


    def select_age(self, selected_val):
        print(selected_val)
        global age
        age = selected_val

    def select_audio_device(self, selected_val):

        print(selected_val)
        print(self.audio_list.index(selected_val))
        br.set_device_index(self.audio_list.index(selected_val))

    def greet(self):
        print("Greetings!")

    def start_recording(self):
        print("starting to record audio")
        global person_name
        person_name = self.name_input.get()
        print("Recording the audoio of " + person_name)
        with Listener(on_release=on_released, on_press=on_pressed) as self.listener:
            try:
                self.listener.join()
            except Exception as e:
                print("Exception hit" + str(e))
                self.stop_recording()

    def stop_recording(self):
        global df, data_filename
        df.to_csv(data_filename, index=False, sep=",")
        print("stopped recording audio")


if __name__ == "__main__":
    print("main")
    root = Tk()

    my_gui = RecordingGui(
        root,
        [p.get_device_info_by_index(i).get("name") for i in range(p.get_device_count()) if
         int(p.get_device_info_by_index(i).get("maxInputChannels") != 0)]
    )
    root.mainloop()
