import streamlit as st
from PIL import Image
import cv2
import matplotlib.pyplot as plt

def imageupload():
    st.title("Image Upload")
    uploaded_files = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"], accept_multiple_files = True)
    if uploaded_files is not None:
            for image in uploaded_files:
                 img = Image.open(image)

def plot_image():
    fig, ax = plt.subplots(imageupload())
    ax.imshow()
    ax.set_title("Interactive Matplotlib Figure")
    ax.set_axis_off()  # Turn off axis for better appearance
    return fig

# Define UI for image upload and display
def app():
    st.title("Streamlit App with Interactive Matplotlib Figure")

    # Display the image using Matplotlib in Streamlit
    fig = plot_image()

    # Display the Matplotlib figure in the Streamlit app
    st.pyplot(fig)

if __name__ == '__main__':
    app()