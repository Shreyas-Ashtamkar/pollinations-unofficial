from time import sleep
import streamlit as st
from streamlit_local_storage import LocalStorage

local_storage = LocalStorage()

def wait_seconds(progress_text, seconds):
    seconds -= 1
    my_bar = st.progress(0, text=progress_text)
    with my_bar:
        for i in range(1, seconds*10+1):
            progress_value = i*100//(seconds*10)
            my_bar.progress(progress_value, text=progress_text)
            sleep(0.1)
    sleep(1)
    my_bar.empty()
