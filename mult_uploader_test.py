
import streamlit as st
from PIL import Image

import streamlit as st
from PIL import Image

# Function to load and display the image
def load_image(image_file):
    img = Image.open(image_file)
    st.image(img, use_column_width=True)

# Main function
def main():
    st.title('Image Viewer')

    # Define a dictionary to store image names and their corresponding file objects
    images = {}

    # File uploader
    uploaded_files = st.sidebar.file_uploader("Upload Image Files", accept_multiple_files=True)

    # Add uploaded files to images dictionary
    if uploaded_files:
        for uploaded_file in uploaded_files:
            images[uploaded_file.name] = uploaded_file

    # Sidebar to select image
    selected_image = st.sidebar.selectbox("Select Image", list(images.keys()), index=0)

    # Display selected image
    if selected_image:
        load_image(images[selected_image])

if __name__ == '__main__':
    main()
