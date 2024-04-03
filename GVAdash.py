import dash
import numpy as np
from dash_canvas import DashCanvas
from dash import Dash, dcc, html, Input, Output, no_update, callback, dash_table, ctx, ALL, MATCH
from dash.dependencies import Input, Output, State
from dash_canvas.utils import array_to_data_url, image_string_to_PILImage
import plotly.express as px
from skimage import data
import json
from dash.exceptions import PreventUpdate
from PIL import Image
import io
import base64

app = dash.Dash(__name__,suppress_callback_exceptions=True,prevent_initial_callbacks=True)

canvas_width = 1250
columns = ['type', 'width', 'height', 'left','top', 'scaleX', 'strokeWidth']

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Label('# Pipette tips per FOV: ' ),
    dcc.Input(
        id='input-number',
        type='number',
        value=3
    ),
    html.Div(id= 'value-container'),
    html.Div(id='output-image-upload'),
    html.Div(id='cropped-image-container'),
    html.Div(id='annotation-container'),
    html.Div(id='GVA-data')
    ])

@app.callback(
    Output('value-container', 'children'),
    [Input('input-number', 'value')]
)
def update_output_div(input_value):
    global Value
    Value = input_value
    return f'Pipettes: {Value}'

def rotator(img):
    width, height = img.size
    if height > width:
        image = img.rotate(90, expand = True)
    return image

def parse_contents(contents, filename, date):
    img = image_string_to_PILImage(contents)
    img = rotator(img)
    pix = np.array(img)
    img_content = array_to_data_url(pix)

    return html.Div([DashCanvas(id='canvaas-image',
                                image_content=img_content,
                                tool='line',
                                lineWidth=5,
                                lineColor='red',
                                width=canvas_width,
                                goButtonTitle='Crop Images')])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('cropped-image-container','children'),
              Input('canvaas-image','json_data'),
              Input('canvaas-image','image_content'),prevent_initial_call=True)
def cropper(json_data,img):
    if json_data:
        data = json.loads(json_data)
        cropped_images = []
        if 'objects' in data:
            objects = data['objects']
            items = len(objects)-1
            left,top,width,height = [],[],[],[]
            for i in range(items):
                if len(objects) > 0 and objects[1]['type'] == 'rect':
                    rect = objects[i+1]
                    left.append(rect.get('left', i))
                    top.append(rect.get('top', i))
                    width.append(rect.get('width', i))
                    height.append(rect.get('height', i))
                    print("Rectangle coordinates:", left, top, width, height)
                    if left[i] >= 0 and top[i] >= 0 and width[i] > 0 and height[i] > 0:
                        image = image_string_to_PILImage(img)
                        widthImage, heightImage = image.size
                        scale = widthImage/canvas_width
                        cropped_img_data = image.crop((left[i]*scale,top[i]*scale,scale*(left[i]+width[i]),scale*(top[i]+height[i])))
                        imagepix = np.array(cropped_img_data)
                        cropped_img_content = array_to_data_url(imagepix)
                        cropped_images.append(html.Div([
                            html.H3(f'Cropped Image {i + 1}'),
                            DashCanvas(id=f'cropped-image-{i}',
                                    image_content=cropped_img_content,
                                    tool='circle',
                                    lineWidth=5,
                                    lineColor='red',
                                    width=canvas_width,
                                    hide_buttons=['save'])
                        ]))
    return cropped_images

@app.callback(Output('annotation-container', 'children'),
            [Input(f'cropped-image-{i}', 'json_data') for i in range(3)],prevent_initial_call=True)
def update_annotation_table(*json_data):
    table_data = []
    for i, data in enumerate(json_data, start=1):
        if data:
            # Retrieve annotation information from JSON data
            objects = json.loads(data).get('objects', [])
            for obj in objects:
                table_data.append({
                    'Canvas Index': i,
                    'Annotation Type': obj.get('type', ''),
                    'Width': obj.get('width', ''),
                    'Height': obj.get('height', ''),
                    'Left': obj.get('left', ''),
                    'Top': obj.get('top', ''),
                    'ScaleX': obj.get('scaleX', ''),
                    'Stroke Width': obj.get('strokeWidth', '')
                })
#put in code to calculate gva here - first, pull from canvas index, then use type to find pipette tip length
#then, use left of all path/circle objects to calculate the gva math
    for i in range(3):
        table_data = table_data['Canvas Index' == {i}]
        

    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in table_data[0].keys()])),
        html.Tbody([
            html.Tr([html.Td(row[col]) for col in row.keys()]) for row in table_data
        ])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)