import streamlit as st
from PIL import Image

# Main title
st.title("Multiple Image Viewer")

# Upload multiple images
uploaded_images = st.file_uploader("Upload image files here", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Initialize session state to store uploaded images
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

# Process uploaded images
if uploaded_images:
    for uploaded_image in uploaded_images:
        st.session_state.uploaded_images.append(uploaded_image)

# Display image and buttons
if st.session_state.uploaded_images:
    # Show the current image index
    if 'image_index' not in st.session_state:
        st.session_state.image_index = 0
    
    # Display the current image
    current_image = st.session_state.uploaded_images[st.session_state.image_index]
    st.image(current_image, caption=f"Image {st.session_state.image_index + 1}/{len(st.session_state.uploaded_images)}", use_column_width=True)

    # Button to display the previous image
    if st.session_state.image_index > 0:
        if st.sidebar.button("Previous Image"):
            st.session_state.image_index -= 1

    # Button to display the next image
    if st.session_state.image_index < len(st.session_state.uploaded_images) - 1:
        if st.sidebar.button("Next Image"):
            st.session_state.image_index += 1
