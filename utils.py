from time import sleep
import streamlit as st
import urllib


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

def aggressive_urlencode(inp: str) -> str:
    return (
        urllib.parse.quote(inp, safe='')
        .replace('-', '%2D')
        .replace('.', '%2E')
        .replace('_', '%5F')
        .replace('~', '%7E')
    )