
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt




import streamlit as st
from streamlit_cropper import st_cropper

# Define UI for image upload and display
def app():
    st.title("GVA-holes")

# Upload image through Streamlit
uploaded_images = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], accept_multiple_files= True)
if uploaded_images is not None:
    for uploaded_image in uploaded_images:
        image = Image.open(uploaded_image)
    # Display the original image
        st.image(image, caption="Uploaded Image", use_column_width=True)
    # Define a placeholder for cropped image
        cropped_image = None
    # Use st_cropper for interactive cropping
        cropped_image = st_cropper(image, box_color="red")
    # Display the cropped image
        st.image(cropped_image, caption="Cropped Image", use_column_width=True)

if __name__ == '__main__':
    app()

print("Hello Argudit")