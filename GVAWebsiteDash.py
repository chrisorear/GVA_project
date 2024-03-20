import dash
import numpy as np
from dash_canvas import DashCanvas
from dash import Dash, dcc, html, Input, Output, no_update, callback, dash_table
from dash.dependencies import Input, Output, State
from dash_canvas.utils import array_to_data_url, image_string_to_PILImage
import plotly.express as px
from skimage import data
import json
from dash.exceptions import PreventUpdate
from PIL import Image
import io
import base64
from dash import dcc

app = dash.Dash(__name__,suppress_callback_exceptions=True)

#defines canvas width and number of columns in json data table
canvas_width = 1250
columns = ['type', 'width', 'height', 'left', 'top', 'scaleX', 'strokeWidth']

#upload function, data table output defined, also style of website
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
    html.Div(id='output-image-upload'),
    dash_table.DataTable(id='canvaas-table',
              style_cell={'textAlign': 'left'},
              columns=[{"name": i, "id": i} for i in columns]),
])

#image prep - convert uploaded image to np array and return html image on dash canvas
def parse_contents(contents, filename, date):
    img = image_string_to_PILImage(contents)
    pix = np.array(img)
    img_content = array_to_data_url(pix)
    return html.Div([DashCanvas(id='canvaas-image',
                                image_content=img_content,
                                tool='line',
                                lineWidth=5,
                                lineColor='red',
                                width=canvas_width)])

#callback updates the original image
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
    
#callback updates the drawings on the original image
@app.callback(Output('canvaas-table', 'data'),
              Input('canvaas-image', 'json_data'))
def update_data(string):
    if string:
        data = json.loads(string) 
    else:
        raise PreventUpdate
    return data['objects'][1:]

for i in dash_table:    
    if dash_table['type'] == 'rect':
        top = i['top']
        bottom = i['top'] + i['height']
        left = i['left']
        right = i['left'] + i['width']
        print (top, bottom, left, right)
        

if __name__ == '__main__':
    app.run_server(debug=True)

#py -m streamlit run "C:\Users\argud\OneDrive\Desktop\Spring 2024\Senior Design\Website Code\GVAWebsite.py"