from ButtonRecorder import ButtonRecorder
from pynput.keyboard import Key, Listener

br = ButtonRecorder("test.wav")

with Listener(
        on_press=br.on_pressed(),
        on_release=br.on_released()) as listener:
    "Starting audio recording"
    listener.join()


print("This is a test")