
from PIL import Image, ImageDraw, ImageEnhance
import cv2
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_cropper import st_cropper

# Define UI for image upload and display
def app():
    st.title("GVA-holes")

st.set_page_config(page_title="GVA-holes", page_icon="🖼️")

#function to adjust image brightness and contrast to increase clarity of colonies
def adjust_image(uploaded_image):
    pil_image = Image.open(uploaded_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(pil_image)
    pil_image = enhancer.enhance(1.5)
    return pil_image

# Upload image through Streamlit
uploaded_images = st.file_uploader("Upload image files here", type=["jpg", "jpeg", "png"], accept_multiple_files= True)

if uploaded_images is not None:
    for uploaded_image in uploaded_images:
        file_name = uploaded_image.name

        #open and adjust image
        adjusted_image = adjust_image(uploaded_image)
        
        # Display the adjusted image with all three pipette tips
        #st.image(adjusted_image, caption=file_name, use_column_width=True)
        # Define a placeholder for cropped image
        cropped_image = None
        cropped_image_name1 = "Top Pipette" + " " + file_name
        cropped_image_name2 = "Middle Pipette" + " " + file_name
        cropped_image_name3 = "Bottom Pipette" + " " + file_name
         # Use st_cropper for interactive cropping
        cropped_image1 = st_cropper(adjusted_image, box_color="red")
        cropped_image2 = st_cropper(adjusted_image, box_color="blue")
        cropped_image3 = st_cropper(adjusted_image, box_color ="green")
    # Display the cropped image
        st.image(cropped_image1, caption=cropped_image_name1, use_column_width=True)
        st.image(cropped_image2, caption=cropped_image_name2, use_column_width=True)
        st.image(cropped_image3, caption=cropped_image_name3, use_column_width=True)

if __name__ == '__main__':
    app()