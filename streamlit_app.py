import pollinations
from pollinations import ImageModel
import streamlit as st
from time import sleep, time
from urllib.parse import quote

from fractions import Fraction

from utils import local_storage, wait_seconds

IMAGE_SIZE_STEP = 128
IMAGE_SIZE_MIN = 128
IMAGE_SIZE_MAX = 2048

if not 'aspect_ratio_locked' in st.session_state:
    st.session_state.aspect_ratio_locked = False

if not 'aspect_ratio' in st.session_state:
    st.session_state.aspect_ratio = 1
    st.session_state.img_height = 256
    st.session_state.img_width  = 256

def toggle_aspect_ratio_lock():
    st.session_state.aspect_ratio_locked = not st.session_state.aspect_ratio_locked

with st.sidebar:
    st.header("Options")
    model  = st.radio("**Models**", options=pollinations.image_models())
    
    if st.session_state.aspect_ratio_locked:
        st.session_state.img_height = st.session_state.img_width*st.session_state.aspect_ratio
        
    st.session_state.img_width  = int(min(IMAGE_SIZE_MAX,max(IMAGE_SIZE_MIN,int(st.session_state.img_width))))
    st.session_state.img_height = int(min(IMAGE_SIZE_MAX,max(IMAGE_SIZE_MIN,int(st.session_state.img_height))))
    
    st.session_state.img_width  = st.slider(
        "**Image Width**",
        min_value=IMAGE_SIZE_MIN,
        max_value=IMAGE_SIZE_MAX,
        value=st.session_state.img_width,
        step=IMAGE_SIZE_STEP
    )
    
    st.session_state.img_height  = st.slider(
        "**Image Height**", 
        min_value=IMAGE_SIZE_MIN, 
        max_value=IMAGE_SIZE_MAX, 
        value= st.session_state.img_height,
        step=IMAGE_SIZE_STEP, 
        disabled=st.session_state.aspect_ratio_locked
    )
    
    st.session_state.aspect_ratio = Fraction(st.session_state.img_height, st.session_state.img_width).real
    
    st.write("Aspect Ratio :", st.session_state.aspect_ratio)
    st.checkbox(f"Lock aspect ratio", on_change=toggle_aspect_ratio_lock, value=st.session_state.aspect_ratio_locked)
    
    seed   = st.text_input("**Seed**", value="-1").strip()

try:
    ai: object = ImageModel()
except Exception as e:
    print(e.__str__())

st.title("Pollinations AI", anchor="https://pollinations.ai/")

st.text("Enter a prompt to generate an Image. Elaborate the scenary as much as possible.")

if prompt:=st.text_input("Prompt", placeholder="Describe the image you want to generate."):
    with st.container(border=True):
        try:
            img = ai.generate(
                prompt=prompt,
                model=model,
                width=st.session_state.img_width,
                height=st.session_state.img_height,
                seed = 'random' if seed == '-1' else int(seed),
            )
            st.image(image=img.content)
        except Exception as e:
            print(e)
            st.toast(e.__str__())
            st.markdown(f"![{prompt}](https://image.pollinations.ai/prompt/{quote(prompt)}?model={model}&width={st.session_state.img_width}&height={st.session_state.img_height}&seed={seed}&nologo=poll&nofeed=yes)")
            
        st.caption(prompt)
    wait_seconds("Cooldown 10s", 10)
