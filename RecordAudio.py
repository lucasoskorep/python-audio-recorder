from ButtonRecorder import ButtonRecorder
from pynput.keyboard import Key, Listener

br = ButtonRecorder()

with Listener(
        on_press=br.on_pressed(),
        on_release=br.on_released()) as listener:
    listener.join()
