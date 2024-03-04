import streamlit as st
import json
from PIL import Image

st.set_page_config(page_title="HEIC Uploader Test", page_icon="🖼️", layout="wide")

st.title("HEIC Uploader")

uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "HEIC"])

def image_converter(uploaded_image):
    image = Image.open(uploaded_image)
    image.convert('RGB').save('example.jpg')
    return image

image_converter(uploaded_image)
st.image(uploaded_image)