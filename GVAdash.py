import dash
import numpy as np
from dash_canvas import DashCanvas
from dash import Dash, dcc, html, Input, Output, no_update, callback, dash_table, ctx, ALL, MATCH
from dash.dependencies import Input, Output, State
from dash_canvas.utils import array_to_data_url, image_string_to_PILImage
import dash_bootstrap_components as dbc
import plotly.express as px
from skimage import data
import json
from dash.exceptions import PreventUpdate
from PIL import Image
import io
import base64

app = dash.Dash(__name__,suppress_callback_exceptions=True,prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.YETI])
canvas_width = 1250

app.layout = html.Div([
    dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("GVA-Holes", className="m1-2",style={'margin-left': '20px'})),
                ],
                align="center",
            ),
            href="/",
        ),
        dbc.Nav(
            dbc.NavItem(dbc.NavLink("About", href="about")),
            navbar=True,
        ),
    ],
    color="primary",
    dark=True,
),
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
    html.Label('Enter volume (uL): ', style = {'margin-left':'20px'}),
    dbc.Input(id='volume-input', type='number', value = 150, size = 'sm', style = {'width': '300px', 'margin-left':'20px'}),
    html.Label('Enter dilution factor: ', style = {'margin-left':'20px'}),
    dbc.Input(id='dilution-input', type='number', value = 100, size = 'sm', style = {'width': '300px', 'margin-left':'20px'}),
    dcc.Tabs(id='image-tabs', style={'margin-left': '20px'}),
    html.Div(id='cropped-image-container'),
    html.Div(id='annotation-container'),
    html.Div(id='GVA-data'),
    ])


#def rotator(img):
 #   width, height = img.size
   # if height > width:
   #     image = img.rotate(90, expand = True)
    #return image

def parse_contents(contents, filename, date):
    img = image_string_to_PILImage(contents)
    width, height = img.size
    if height > width:
        img = img.rotate(90, expand=True)
    pix = np.array(img)
    img_content = array_to_data_url(pix)

    return html.Div([DashCanvas(id='canvaas-image',
                                image_content=img_content,
                                tool='line',
                                lineWidth=5,
                                lineColor='red',
                                width=canvas_width,
                                goButtonTitle='Crop Images')])


@app.callback(Output('image-tabs', 'children'),
              Input('upload-image', 'contents'))
def update_image_tabs(contents):
    if contents is not None:
        children = []
        for i, content in enumerate(contents):
            children.append(dcc.Tab(id={'type': 'image-tabs', 'index': i},label=f'Image {i + 1}', value=f'image-{i + 1}', children=[
                parse_contents(content, None, None)
            ]))
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
                    if left[i] >= 0 and top[i] >= 0 and width[i] > 0 and height[i] > 0:
                        image = image_string_to_PILImage(img)
                        widthImage, heightImage = image.size
                        scale = widthImage/canvas_width
                        cropped_img_data = image.crop((left[i]*scale,top[i]*scale,scale*(left[i]+width[i]),scale*(top[i]+height[i])))
                        imagepix = np.array(cropped_img_data)
                        cropped_img_content = array_to_data_url(imagepix)
                        cropped_images.append(html.Div([
                            html.H4(f'Cropped Image {i + 1}'),
                            DashCanvas(id={'type': 'cropped-image', 'index': i},
                                    image_content=cropped_img_content,
                                    tool='circle',
                                    lineWidth=5,
                                    lineColor='red',
                                    width=canvas_width,
                                    hide_buttons=['save'])
                        ]))
        return cropped_images

@app.callback(Output('annotation-container', 'children'),
              Input({'type':'cropped-image', "index": ALL}, 'json_data'),
              Input('volume-input','value'),
              Input('dilution-input','value'),
              prevent_initial_call=True)
def update_annotation_table(json_data, V, df):
    table_data = []
    CFUs = []
    for i, data in enumerate(json_data, start=1):
        if data:
            # Retrieve annotation information from JSON data
            objects = json.loads(data).get('objects', [])
            line_count = 0
            pipette_length = []
            colony_loc = []
            for obj in objects:
                # Check if the object is a line
                if obj.get('type') == 'line':
                    # Increment line count
                    line_count += 1
                    # Append annotation information to table_data
                    pipette_length.append(int(obj.get('left',0)))
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
                #If the object is a point, then append the position to the colony_loc list
                elif obj.get('type') == 'path' or obj.get('type') == 'circle':
                    colony_loc.append(int(obj.get('left',0)))
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
                else:
                    no_update
            #GVA calculation
            if len(colony_loc) >= 1 and line_count == 2:
                x1 = pipette_length[0]
                x2 = pipette_length[1]
                h = abs(x2 - x1)
                CFUs.append(df*len(colony_loc)/(V/1000*np.absolute(np.power(x2,3)-np.power(x1,3))/np.power(h,3)))
                print(CFUs)
                print(i)

#put in code to calculate gva here - first, pull from canvas index, then use type to find pipette tip length
#then, use left of all path/circle objects to calculate the gva math
# Generate a table to display annotation information
    if table_data:
        annotation_table = dash_table.DataTable(
            id='annotation-table',
            columns=[{'name': col, 'id': col} for col in table_data[0].keys()],
            data=table_data
        )
    else:
        annotation_table = html.Div("No annotation data available.")


    # Generate an HTML component to display CFUs
    cfu_html = [html.Div(html.H5(f'Cropped Image {i + 1}: {float(CFUs[i])} CFUs/mL')) for i in range(len(CFUs))]

    # Return the annotation table and CFUs HTML components
    return [annotation_table] + cfu_html


if __name__ == '__main__':
    app.run_server(debug=True)