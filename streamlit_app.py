# import pollinations
# import pollinations.models
from pollinations.models import ImageModel
import streamlit as st
from time import sleep, time
from urllib.parse import quote

from utils import local_storage, wait_seconds

with st.sidebar:
    st.header("Options")
    model  = st.radio("**Models**", options=ImageModel.models)
    height = st.slider("**Image Height**", min_value=100, max_value=2048, value=128)
    width  = st.slider("**Image Width**", min_value=100, max_value=2048, value=128)
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
                width=width,
                height=height,
                seed = 'random' if seed == '-1' else int(seed),
            )
            st.image(image=img.content)
        except Exception as e:
            print(e)
            st.toast(e.__str__())
            st.markdown(f"![{prompt}](https://image.pollinations.ai/prompt/{quote(prompt)}?model={model}&width={width}&height={width}&seed={seed}&nologo=poll&nofeed=yes)")
            
        st.caption(prompt)
    wait_seconds("Cooldown 10s", 10)
