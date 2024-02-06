
from PIL import Image, ImageDraw, ImageEnhance
import cv2
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_cropper import st_cropper
from streamlit_drawable_canvas import st_canvas

#Put instructions for the user
instructions1 = "Welcome to the GVA-holes website. If you are reading this, you're probably a super cool person that loves to calculate bacterial concentrations. If so, please follow the instructions below:"
instructions2 = "First, you'll upload your image. It will show up three times. On the first one, move the red crop box so that it is fully around the top pipette. On the second one, move the blue crop box so that it is fully around the middle pipette in the image. On the third, move the green crop box so that it is fully around the bottom pipette in the image."


#configure webpage
st.set_page_config(page_title="GVA-holes", page_icon="🆘", layout="wide")

#all functions are here
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
        st.markdown("Please draw a red box around the top pipette in the image below, then double click to crop.")
        cropped_image1 = st_cropper(adjusted_image, box_color="red", realtime_update=False)
        st.markdown("Please draw a blue box around the middle pipette in the image below, then double click to crop.")
        cropped_image2 = st_cropper(adjusted_image, box_color="blue", realtime_update= False)
        st.markdown("Please draw a green box around the bottom pipette in the image below, then double click to crop.")
        cropped_image3 = st_cropper(adjusted_image, box_color ="green", realtime_update=False)
    # Display the cropped image
        #cropped_image_1 = st.image(cropped_image1, caption=cropped_image_name1, use_column_width=True)
        #cropped_image_2 = st.image(cropped_image2, caption=cropped_image_name2, use_column_width=True)
        #cropped_image_3 = st.image(cropped_image3, caption=cropped_image_name3, use_column_width=True)

#Code to make the cropped images drawable
# Initialize the canvas
        # Specify canvas parameters in application
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
        )

        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        point_display_radius = 0
        stroke_color = ""
        bg_color = ""
        bg_image = cropped_image1
        realtime_update = st.sidebar.checkbox("Update in realtime", True)

        if drawing_mode == 'point':
            point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
            stroke_color = st.sidebar.color_picker("Stroke color hex: ")
            bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

        if drawing_mode == 'line':
            line_display_radius = st.sidebar.slider("Line display radius: ", 1, 25, 3)
            stroke_color = st.sidebar.color_picker("Stroke color hex: ")
            bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

        width1, height1 = cropped_image1.size
        aspect_ratio1 = width1 / height1

        width2, height2 = cropped_image2.size
        aspect_ratio2 = width2 / height2

        width3, height3 = cropped_image3.size
        aspect_ratio3 = width3 / height3
        
        # Create a canvas component for each image
        canvas_result1 = st_canvas(
            fill_color="rgba(255, 255, 255, 0)", # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=bg_image,
            update_streamlit=realtime_update,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius if drawing_mode == "point" else 0,
            display_toolbar=st.sidebar.checkbox("Display toolbar", True),
            height = 700 / aspect_ratio1,
            width = 700,
            key = None
        )


