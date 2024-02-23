import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance
from streamlit_drawable_canvas import st_canvas
from streamlit_cropper import st_cropper

#Put instructions for the user - TO DO
Intro = "If you’re here, you must be someone who loves to find bacteria concentrations on a budget. Who needs MATLAB anyway? Before you go on to use the website, please read the instructions carefully. Any further questions can be directed to gvahelp@gmail.com. We sincerely hope you enjoy the website. -	A couple of GVA-holes"
Instructions = "Instructions: First, upload your images (maximum of three at a time as of 2/22/24). First, set the number of crop regions to the number of pipette tips per image. Then, place the crop boxes around each pipette tip in the images that load. Finally, scroll down to below the images where the cropped pipette tips appear. Click once at the very end of the pipette tip, and once at the top of the agarose gel inside of the tip. Then, select 5-10 colonies as close to the tip as possible. Finally, press the Send to Streamlit button just below the bottom left of the image and record the results that appear."

#configure webpage
st.set_page_config(page_title="GVA-holes", page_icon="🆘", layout="wide")
st.markdown(Intro)
st.markdown(Instructions)
#all functions are here
#function to adjust image brightness and contrast to increase clarity of colonies
def adjust_image(uploaded_image):
    pil_image = Image.open(uploaded_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(pil_image)
    pil_image = enhancer.enhance(1.5)
    return pil_image
#function to make the cropped images drawable
def canvas(cropped_image):
    drawing_mode = "point"
    width1, height1 = cropped_image.size
    stroke_width = 1
    point_display_radius = 0.5
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
        height = 1000 / aspect_ratio1,
        width = 1000,
        key = f"{i}" + f"{file_name}"
        )
    return canvas_result1
#function to crop images into 3 separate things
def image_cropper(num_regions):
    for i in range(num_regions):
        st.subheader(f"{file_name}" + " " + f"Crop Region {i+1}")
        box_coords = (0, width1, (i)/3*height1, (i+1)/3*height1)
        # Perform cropping with a unique key for each st_cropper widget
        cropped_images.append(st_cropper(adjusted_image, default_coords = box_coords, key=f"cropper_{i}" + f"{file_name}"))
    return cropped_images   
#function to pull colony location from canvas as you click on colonies
def colonyfunc(drawable):            
    if drawable.json_data is not None:
        colonies = []
        objects = pd.json_normalize(drawable.json_data["objects"]) # need to convert obj to str because PyArrow
        for col in objects.select_dtypes(include=['object']).columns:
            left = objects["left"].astype("double")
            colonies = left.tolist()
            return colonies           
#function to do GVA calculations from the clicked colony data
def GVAcalc(colonies):
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
        x1 = np.max(colonies)*convertH
        CFUs = len(colonies)/(np.absolute((np.power(x2,3) - np.power(x1,3)))/(1000*(3*36^2)*np.pi*1.995))
        st.write("CFUs/mL",CFUs)


# Upload image through Streamlit
uploaded_images = st.file_uploader("Upload image files here", type=["jpg", "jpeg", "png"], accept_multiple_files= True)
num_regions = st.number_input("Number of regions to crop:", min_value=1, max_value=10, value=3)

if uploaded_images is not None:
    for uploaded_image in uploaded_images:
        current_image = uploaded_image
        file_name = current_image.name
        #open and adjust image
        adjusted_image = adjust_image(current_image)
        width1, height1 = adjusted_image.size
        cropped_images = []
        cropped_images = image_cropper(num_regions)
        for i, image in enumerate(cropped_images):
            drawable = canvas(image)
            colonies = colonyfunc(drawable)
            st.write(colonies)
            if colonies is not None:
                GVAcalc(colonies)
        
