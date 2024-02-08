import streamlit as st
from PIL import Image

# Function to initialize session state
def init_session_state():
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []

# Function to process uploaded images
def process_uploaded_images(uploaded_images):
    for uploaded_image in uploaded_images:
        st.session_state.uploaded_images.append(uploaded_image)

# Function to display the current image
def display_image(image_index):
    if st.session_state.uploaded_images:
        current_image = st.session_state.uploaded_images[image_index]
        st.image(current_image, caption=f"Image {image_index + 1}/{len(st.session_state.uploaded_images)}", use_column_width=True)

# Main title
st.title("Multiple Image Viewer")

# Initialize session state
init_session_state()

# Upload multiple images
uploaded_images = st.file_uploader("Upload image files here", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Process uploaded images
if uploaded_images:
    process_uploaded_images(uploaded_images)

# Show the current image index
if 'image_index' not in st.session_state:
    st.session_state.image_index = 0

# Display the current image
display_image(st.session_state.image_index)

# Button to display the previous image
if st.session_state.image_index > 0:
    if st.button("Previous Image"):
        st.session_state.image_index -= 1

# Button to display the next image
if st.session_state.image_index < len(st.session_state.uploaded_images) - 1:
    if st.button("Next Image"):
        st.session_state.image_index += 1