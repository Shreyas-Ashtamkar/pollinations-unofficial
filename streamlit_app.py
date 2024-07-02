import pollinations
import streamlit as st
from time import sleep, time

from utils import local_storage, wait_seconds

with st.sidebar:
    st.header("Options")
    model  = st.radio("**Options**", options=pollinations.models)
    height = st.slider("**Image Height**", min_value=100, max_value=2048, value=1024)
    width  = st.slider("**Image Width**", min_value=100, max_value=2048, value=1024)
    seed   = st.text_input("**Seed**", value="-1").strip()

ai: object = pollinations.Model()

st.title("Pollinations AI", anchor="https://pollinations.ai/")

st.text("Enter a prompt to generate an Image. Enter as many details as possible.")

if prompt:=st.text_input("Prompt", placeholder="Describe the image you want to generate."):
    with st.container(border=True):
        img = ai.generate(
            prompt=prompt,
            model=model,
            width=width,
            height=height,
            seed = 'random' if seed == '-1' else int(seed),
        )
        st.image(image=img.binary)
        st.caption(prompt)
    # st.button("Download", type="secondary", on_click=lambda:img.save(prompt.replace(" ", "_")+".jpg"))
    
    wait_seconds("Cooldown 10s", 10)
