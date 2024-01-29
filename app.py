#the file name has to be app.py or else the code won't work

from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import base64

app_ui = ui.page_fluid(
    ui.input_file("image", "Upload image files (.jpg) here", multiple=False),
    ui.output_image("my_images")
)

def server(input, output, session):
    @output
    @render.image
    def my_images():
        if input.images:
            img = Image.open(io.BytesIO(input.image() ["content"]))

            # Save the image temporarily to a BytesIO object
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            # Convert image to base64 for embedding in HTML
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

            # Create an HTML image tag
            img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Uploaded Image">'

            return img_tag

app = App(app_ui, server)