# import pollinations
# import pollinations.models
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

with st.sidebar:
    width  = 256
    
    if 'aspect_ratio' not in st.session_state:
        st.session_state.img_height = 256
        st.session_state.aspect_ratio = st.session_state.img_height/width
        
    st.header("Options")
    model  = st.radio("**Models**", options=pollinations.image_models())
        
    lock_aspect_ratio = st.checkbox(f"Lock aspect ratio")
                
    width   = st.slider("**Image Width**", min_value=IMAGE_SIZE_MIN, max_value=IMAGE_SIZE_MAX, value=width, step=IMAGE_SIZE_STEP)
    st.session_state.img_height  = st.slider(
        "**Image Height**", 
        min_value=IMAGE_SIZE_MIN, 
        max_value=IMAGE_SIZE_MAX, 
        value=int(width*st.session_state.aspect_ratio) if lock_aspect_ratio else st.session_state.img_height, 
        step=IMAGE_SIZE_STEP, 
        disabled=lock_aspect_ratio
    )
    
    st.session_state.aspect_ratio = Fraction(st.session_state.img_height, width).real
    
    st.write("Aspect Ratio : ", str(st.session_state.aspect_ratio))

    seed   = st.text_input("**Seed**", value="-1").strip()

try:
    ai: object = ImageModel()
except Exception as e:
    print(e.__str__())

st.title("Pollinations AI", anchor="https://pollinations.ai/")

st.write("Enter a prompt to generate an Image. Elaborate the scenary as much as possible.")

if 'text_input_locked' not in st.session_state:
    st.session_state.text_input_locked = False

def toggle_input_prompt_lock():
    st.session_state.text_input_locked = not st.session_state.text_input_locked
    print(st.session_state.text_input_locked)

if prompt:=st.text_input("Prompt", placeholder="Describe the image you want to generate.", disabled=st.session_state.text_input_locked, key='text_input'):
    if not st.session_state.text_input_locked:
        toggle_input_prompt_lock()
        
        with st.container(border=True):
            st.markdown(f"![{prompt}](https://image.pollinations.ai/prompt/{quote(prompt)}?model={model}&width={width}&height={st.session_state.img_height}&seed={seed}&nologo=poll&nofeed=yes)")
            st.caption(prompt)

        wait_seconds("Cooldown 10s", 10)
        
        toggle_input_prompt_lock()

#TODO : Fix the line 61 to work 