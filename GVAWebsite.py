import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw
import io
import cv2
import matplotlib.pyplot as plt
import mpld3
import streamlit.components as components
from streamlit_drawable_canvas import st_canvas
from streamlit_cropper import st_cropper
import plotly.graph_objects as go


#Put instructions for the user
instructions1 = "Welcome to the GVA-holes website. If you are reading this, you're probably a super cool person that loves to calculate bacterial concentrations, in other words, you're a GVA-hole. If so, please follow the instructions below:"
instructions2 = "First, you'll upload your image. It will show up three times. On the first one, move the red crop box so that it is fully around the top pipette. On the second one, move the blue crop box so that it is fully around the middle pipette in the image. On the third, move the green crop box so that it is fully around the bottom pipette in the image."

#configure webpage
st.set_page_config(page_title="GVA-holes", page_icon="🆘", layout="wide")
# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

#all functions are here
#function to adjust image brightness and contrast to increase clarity of colonies
def adjust_image(uploaded_image):
    pil_image = Image.open(uploaded_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(pil_image)
    pil_image = enhancer.enhance(1.5)
    return pil_image

#Code to make the cropped images drawable
# Initialize the canvas
        # Specify canvas parameters in application


def canvas(cropped_image):
    drawing_mode = "point"
    width1, height1 = cropped_image.size
    stroke_width = 1
    point_display_radius = 2
    stroke_color = "black"
    bg_color = ""
    aspect_ratio1 = width1 / height1
    bg_image = cropped_image
        # Create a canvas component for each image
    canvas_result1 = st_canvas(
        fill_color="rgba(255, 255, 255, 0)", # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=bg_image,
        update_streamlit=False,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        display_toolbar=True,
        height = 700 / aspect_ratio1,
        width = 700,
        key = f"image_{i}"
        )
    return canvas_result1

# Upload image through Streamlit
uploaded_images = st.file_uploader("Upload image files here", type=["jpg", "jpeg", "png"], accept_multiple_files= True)


if uploaded_images is not None:
    for uploaded_image in uploaded_images:
        file_name = uploaded_image.name

        #open and adjust image
        adjusted_image = adjust_image(uploaded_image)
        num_regions = st.number_input("Number of regions to crop:", min_value=1, max_value=10, value=3)
        width1, height1 = adjusted_image.size
        #box_coords = (0, width1, 2/3*height1, height1)
        cropped_images = []
        j = 0
        for i in range(num_regions):
            st.subheader(f"Crop Region {i+1}")
            box_coords = (0, width1, (i)/3*height1, (i+1)/3*height1)
            # Perform cropping with a unique key for each st_cropper widget
            cropped_images.append(st_cropper(adjusted_image, default_coords = box_coords, key=f"cropper_{i}"))
            # Display the cropped image
            drawable = canvas(cropped_images[i])
            if drawable.json_data is not None:
                colonies = []
                objects = pd.json_normalize(drawable.json_data["objects"]) # need to convert obj to str because PyArrow
                for col in objects.select_dtypes(include=['object']).columns:
                    left = objects["left"].astype("double")
                    colonies = left.tolist()
                #Finds length of pipette tip in pixels
                if len(colonies) >= 2:
                    h = np.max(colonies) - np.min(colonies)
                    convertH = 36/h
                    max = np.max
                    #Removes min and mix values because they are not colonies
                    colonies.remove(max(colonies))
                    colonies.remove(min(colonies))
                    if len(colonies) >= 1:
                        st.write("Pipette Length in pixels", h)
                        st.write("Colony Locations", colonies)
                        x2 = np.min(colonies)*convertH
                        st.write("x2",x2)
                        x1 = np.max(colonies)*convertH
                        CFUs = len(colonies)/(np.absolute((np.power(x2,3) - np.power(x1,3)))/(1000*(3*36^2)*np.pi*1.995))
                        st.write("CFUs/mL",CFUs)