import streamlit as st
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import mpld3
import streamlit.components as components

def imageupload():
    st.title("Image Upload")
    uploaded_files = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"], accept_multiple_files = True)
    if uploaded_files is not None:
            for image in uploaded_files:
                img = Image.open(image)
                fig, ax = plt.subplots()
                ax.imshow(img)
                ax.set_title("Interactive Matplotlib Figure")
                ax.set_axis_off()  # Turn off axis for better appearance
            return fig

def plot_image():
    fig, ax = plt.subplots()
    ax.imshow()
    ax.set_title("Interactive Matplotlib Figure")
    ax.set_axis_off()  # Turn off axis for better appearance
    return fig

# Define UI for image upload and display
def app():
    st.title("Streamlit App with Interactive Matplotlib Figure")
    fig = imageupload()
    # Display the image using Matplotlib in Streamlit
    #fig = plot_image()
    # Display the Matplotlib figure in the Streamlit app
    st.pyplot(fig)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)

if __name__ == '__main__':
    app()

print("Hello Argudit")