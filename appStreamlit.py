import streamlit as st
from PIL import Image

# Define UI for image upload and display
def app():
    st.title("Image Upload")
    uploaded_files = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"], accept_multiple_files = True)
    if uploaded_files is not None:
            for image in uploaded_files:
                img = Image.open(image)
                st.image(image, caption='Uploaded Image.', use_column_width=True)

if __name__ == '__main__':
    app()