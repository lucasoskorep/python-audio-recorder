from ButtonRecorder import ButtonRecorder
from pynput.keyboard import Key, Listener

br = ButtonRecorder("test.wav")

def on_pressed(key):
    print('{0} pressed'.format(
        key))
def on_released(key):
    print('{0} pressed'.format(
        key))

with Listener(
        on_press=on_pressed,
        on_release=on_released) as listener:
    listener.join()


print("This is a test")