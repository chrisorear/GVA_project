import streamlit as st
import json

st.set_page_config(page_title="Multiple Crop Boxes", page_icon="🖼️", layout="wide")

st.title("Multiple Crop Boxes")

uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the original image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True, channels="RGB")

    # Define a unique ID for the canvas
    canvas_id = "canvas"

    # Inject JavaScript code for fabric.js
    st.markdown(
        """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/3.6.3/fabric.min.js"></script>
        <canvas id="canvas" width="500" height="500"></canvas>
        <script>
            var canvas = new fabric.Canvas('canvas');
            var boxes = [];

            function addBox(left, top, width, height) {
                var rect = new fabric.Rect({
                    left: left,
                    top: top,
                    width: width,
                    height: height,
                    fill: 'transparent',
                    stroke: 'red',
                    strokeWidth: 2,
                    selectable: true
                });

                canvas.add(rect);
                boxes.push(rect);
            }

            canvas.on('object:modified', function() {
                var serializedBoxes = JSON.stringify(boxes.map(function(box) {
                    return {left: box.left, top: box.top, width: box.width, height: box.height};
                }));
                Streamlit.setComponentValue(serializedBoxes);
            });
        </script>
        """
    )

    # Placeholder for the serialized crop boxes
    serialized_boxes = st.empty()

    # Get the serialized boxes from the frontend
    boxes_json = serialized_boxes.text()

    # Display the serialized boxes (for debugging)
    st.json(json.loads(boxes_json) if boxes_json else [])

    # Provide a link to open the app in a new tab
    st.markdown("Open this link in a new tab: [Multiple Crop Boxes](http://localhost:8501)")
