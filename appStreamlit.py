import streamlit as st
from PIL import Image

# Define UI for image upload and display
def app():
    st.title("Image Upload")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

if __name__ == '__main__':
    app()