import pollinations
from pollinations import Image #, Text, Async
import streamlit as st
from time import sleep
from urllib.parse import quote

from fractions import Fraction

from streamlit_local_storage import LocalStorage

from utils import wait_seconds

IMAGE_SIZE_STEP = 128
IMAGE_SIZE_MIN = 128
IMAGE_SIZE_MAX = 2048

local_storage = LocalStorage()
sleep(0.5)
local_storage.setItem("generate_image_prompt", None)
sleep(0.5)

with st.sidebar:
    width  = 256
    if 'aspect_ratio' not in st.session_state:
        st.session_state.img_height = 256
        st.session_state.aspect_ratio = st.session_state.img_height/width
    st.header("Options")
    model  = st.radio("**Models**", options=pollinations.Image.models())
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

st.title("Pollinations AI", anchor="https://pollinations.ai/")
st.write("Enter a prompt to generate an Image. Elaborate the scenary as much as possible.")

def generate(prompt:str, model:str, width:int, height:int,seed:int, nologo:str="poll", private:bool=True, nonsfw:bool=True):
    local_storage.setItem("generate_image_prompt", f"https://image.pollinations.ai/prompt/{quote(prompt)}?model={model}&width={width}&height={height}&seed={seed}&nologo={nologo}&private={private}&safe={nonsfw}")
    

prompt = st.text_input(
    label="Prompt",
    placeholder="Describe the image you want to generate.", 
    key='text_input'
)

st.button(
    label="Generate",
    key="generate_button", 
    help="Click on this button to generate the image below", 
    on_click= lambda : generate(
        prompt = prompt,
        model  = model,
        width  = width,
        height = st.session_state.img_height,
        seed   = seed
    ),
)

if img_prompt:=local_storage.getItem("generate_image_prompt"):
    if prompt != "":
        with st.container(border=True):
            st.image(
                image=img_prompt,
                caption=prompt,
                use_container_width =True
            )
    else:
        local_storage.setItem("generate_image_prompt", None)