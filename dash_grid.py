import base64
import datetime
import io
import random

import dash_ag_grid as dag  # pip install dash-ag-grid
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components # https://github.com/facultyai/dash-bootstrap-components
import numpy as np
import pandas as pd
from dash import Dash, Input, Output, State, callback, dash_table, html, dcc
import dash_daq as daq

import plotly.express as px

# Dash is a web application framework that provides pure Python abstraction around HTML, CSS, and JavaScript.
# Dash HTML Components module (dash.html) has a component for every HTML tag. 
# Dash Core Components (dash.dcc) contains higher-level components that are interactive and are generated with JavaScript, HTML, and CSS through the React.js library.

# Dash Acquisition & Controlfor Dash  (daq)
# Dash DAQ comprises a robust set of controls that make it simpler to integrate data acquisition and controls into your Dash applications.
# pip install dash_daq

# open http://127.0.0.1:8050/

def get_data():
    n = 30
    countries = ["US", "CA", "JP"] * n
    # print(countries)
    random.shuffle(countries)
    # print(cats)
    cats = list(["Clothing", "Food", "Electronics"] * n)
    # print(cats)
    random.shuffle(cats)
    # print(cats)
    indata = {
        "Store": ["s1", "s2", "s3"] * n,
        "Country": countries,
        "Cat": cats,
        "Units": list(np.random.random(n * 3) * 1e3),
        "Sales": list(np.random.random(n * 3) * 1e7),
    }
    df = pd.DataFrame(indata)
    # print(df)
    # dfp = df.pivot_table(index='Store', columns=['Country', 'Cat'], values='Sales', aggfunc='sum')
    return df


df = get_data()

colors = {"background": "#111111", "text": "#7FDBFF"}

def get_column_defs():
    columnDefs = [
        {  # Row number
            "headerName": "Row #",
            "maxWidth": 120,
            "rowDrag": True,
            # "valueGetter": {"function": "params.node ? params.node.id : null;"},
            "valueGetter": {"function": "params.node ? params.node.rowIndex : null;"},
        },
        {
            "headerName": "Store",
            "field": "Store",
            "sortable": True,
            "rowGroup": True,
            "enableRowGroup": True,
            "pivot": False,
            "filter": True,
            "rowDrag": False,        
            # Cell Renderer allows you to put whatever HTML
            # https://dash.plotly.com/dash-ag-grid/cell-rendering#provided-cell-renderers
            # 'cellRenderer': 'agCheckboxCellRenderer',
            # stockLink function is defined in the dashAgGridComponentFunctions.js in assets folder
            "cellRenderer": "StockLink",
        },
        
        # By Column Pivot
        {  
            "headerName": "Countries",
            "field": "Country",
            "pivot": True,
            # "cellRendererSelector": {
            #     "function": "customCellRendererSelector(params)"
            # },
        },
        {
            "headerName": "Categories",
            "field": "Cat",
            "pivot": True,
            # "cellRenderer": 'agCheckboxCellRenderer', // Boolean Only
            # value formatters are for text formatting
            # "valueFormatter": {
            #     "function": "params.value ? params.value.toUpperCase() : '' "
            # },
        },
        
        # {  # By Column Hierarchy
        #     "headerName": "CountryCat",
        #     "headerClass": "center-aligned-group-header",
        #     "suppressStickyLabel": True,  # defaults to False
        #     "marryChildren": True,  # always stick together.
        #     "children": [
        #         {
        #             "headerName": "Country",
        #             "field": "Country",
        #             "pivot": True,
        #             "cellRendererSelector": {
        #                 "function": "customCellRendererSelector(params)"
        #             },
        #         },
        #         {
        #             "headerName": "Category",
        #             "field": "Cat",
        #             "pivot": True,
        #             #  'cellRenderer': 'agCheckboxCellRenderer',
        #             # value formatters are for text formatting
        #             "valueFormatter": {
        #                 "function": "params.value ? params.value.toUpperCase() : '' "
        #             },
        #         },
        #     ],
        # },
        # {"headerName": "Country", "field": "Country", "pivot": True},
        # {"headerName": "Category", "field": "Cat", "pivot": True},
        
        {
            "headerName": "Sales",
            "headerClass": "right-aligned-group-header",
            # "suppressStickyLabel": True,
            "openByDefault": True,
            "marryChildren": True,
            "children": [
                {
                    "headerName": "Units (#)",
                    "field": "Units",
                    "type": "rightAligned",
                    "cellDataType": "number",
                    # Formatting Numbers with d3-format
                    # https://observablehq.com/@d3/d3-format
                    "valueFormatter": {"function": "d3.format(',.0f')(params.value)"},
                    # "filter": "agNumberColumnFilter", "columnGroupShow": "closed", # Show / Hide Columns
                    "aggFunc": "sum",
                },            
                {
                    "headerName": "Sales ($)",
                    "field": "Sales",
                    "type": "rightAligned",
                    "cellDataType": "number",
                    # Formatting Numbers with d3-format
                    # https://observablehq.com/@d3/d3-format
                    "valueFormatter": {"function": "d3.format(',.1f')(params.value)"},
                    # "filter": "agNumberColumnFilter", "columnGroupShow": "closed", # Show / Hide Columns
                    "aggFunc": "sum",
                },
                {
                    "headerName": "Sales/Unit",
                    "colId": "goldSilverRatio",
                    "type": "rightAligned",
                    "aggFunc": {"function": "ratioAggFunc(params)"},
                    "valueGetter": {"function": "ratioValueGetter(params)"},
                    "valueFormatter": {"function": "ratioFormatter(params)"},
                },            
                # Value Getters - Derived columns
                {
                    "headerName": "Sales in M ($)",
                    "minWidth": 10,
                    "type": "rightAligned",
                    "valueGetter": {"function": "params.data.Sales / 1e6"},
                    # Formatting Numbers with d3-format
                    "valueFormatter": {"function": "d3.format('($,.1f')(params.value)"},
                    "filter": "agNumberColumnFilter",
                    "columnGroupShow": "closed",
                },
                # # Value Getters - Derived columns
                # {
                #     "headerName": "Sales in M (EUR}",
                #     "minWidth": 10,
                #     "type": "rightAligned",
                #     "valueGetter": {"function": "params.data.Sales / 1e6"},
                #     # Formatting Numbers with d3-format
                #     "valueFormatter": {"function": "EUR(params.value)"},
                #     "filter": "agNumberColumnFilter",
                #     "columnGroupShow": "open",
                # },
            ],
        },
    ]
    return columnDefs   

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Dash app
app = Dash(
    __name__,
    title='My VS Store Dash Analytics',
    #    external_stylesheets=external_stylesheets,
    #    assets_external_path='http://your-external-assets-folder-url/'
)

app.renderer = """
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log(payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log(payload);
        console.log(response);
    }
})
"""

data = {}

def make_charts(df):
    fig = px.scatter(df, x="Units", y="Sales", color="Country", custom_data=["Sales"]
                     )
    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=20)
    return fig

fig = make_charts(df)

def make_layout():
    """
        The layout is composed of a tree of "components" such as html.Div and dcc.Graph. 
    """
    layout = html.Div([
            html.H1(
                children="My VS Store Dash App",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            html.Br(),
            # dcc.Dropdown(df.Store.unique(), 'S1', id='dropdown-selection'),
            html.Br(),
            html.Div([
                dcc.Input(id='input-1-state', type='text', value='Montréal'),
                dcc.Input(id='input-2-state', type='text', value='Canada'),
                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                html.Div(id='output-state')
            ]),
            
            html.Br(),
            html.Div([
                dcc.Upload(
                    id='upload-data',
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
                html.Div(id='output-data-upload'),
            ]),
            html.Br(),
            
            html.H4(children="Summary"),
            html.Div(
                id="pivot-table-div",
                children=[
                    dag.AgGrid(
                        id="pivot-table-container",
                        enableEnterpriseModules=True,
                        # licenseKey = os.environ['AGGRID_ENTERPRISE'],
                        rowData=df.to_dict("records"),
                        columnDefs=get_column_defs(),
                        # columnDefs=[{"field": i} for i in df.columns],
                        defaultColDef={
                            "resizable": True,
                            "sortable": True,
                            "filter": False,
                            "useValueFormatterForExport": True,
                            "initialWidth": 200,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                        },
                        columnSize="sizeToFit",  # autoSize sizeToFit # Dash only option
                        dashGridOptions={
                            "pivotMode": False, # Enable Pivot
                            "animateRows": True,
                            "rowSelection": "multiple",  # single
                            "enableBrowserTooltips": True,
                            "pagination": False,
                            # "paginationPageSize": 5,
                            "paginationAutoPageSize": False,
                            "rowDragManaged": True,  # drag does not work with paging
                            "rowDragMultiRow": True,
                            # 'isRowSelectable': {"function": "log(params)"} # pass to JS
                            # 'isRowSelectable': {"function": "params.data ? params.Store == 's2' : false"}
                            "suppressAggFuncInHeader": True,
                            # "sideBar": True,
                        },
                        # https://www.ag-grid.com/archive/31.0.2/example/
                        className="ag-theme-alpine-dark",  # interactions saved after refresh
                        persistence=True,
                        csvExportParams={                
                            "fileName": "ag_grid_test.csv",
                        },
                    ),
                ],
            ),
            html.Button("Download CSV", id="csv-button", n_clicks=0),
            html.Br(),
            daq.BooleanSwitch(id='our-boolean-switch', on=False),
            html.Div(id='boolean-switch-result'),

            html.Hr(),
            
            html.H4(children="Details"),
            
            # html.Div([
            #     "Input: ",
            #     dcc.Input(id='my-input', value='initial value', type='text')
            # ]),
            # html.Div(id='my-output'),
            
            # generate_table(df),
            
            html.Div(
                id="detail-table-div1",
                children=[
                    dag.AgGrid(
                        id="detail-grid-container",
                        columnDefs=[{"field": i} for i in df.columns],
                        rowData=df.to_dict("records"),
                    )
                ],
            ),
            # html.Div(
            #     id="detail-table-div2",
            #     children=[
            #         dash_table.DataTable(
            #             id="detail-table-container",
            #             columns=[{"name": i, "id": i} for i in df.columns],
            #             data=df.to_dict("records"),
            #             # style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'}
            #             page_action="native",
            #             page_size=10,
            #         )
            #     ],
            # ),
            
            dcc.Graph(
                id='basic-interactions',
                figure=fig
            ),
                
            dbc.Alert(id="tbl_out"),
        ],
        style={"margin": 20},
    )
    return layout

app.layout = make_layout()

# Reactive @callback
# Listen to firing in Input() comp property and pass the return to Output()
# Pass extra values with State() from other comp 

# @callback(
#     Output(component_id='my-output', component_property='children'),
#     Input(component_id="pivot-table-container", component_property="selectedRows"),
#     Input(component_id='my-input', component_property='value'),
# )
# def update_output_div(selected, initValue):
#     return f'Selected Row: {selected or initValue}'

@callback(
    # Output(component_id="detail-table-container", component_property="data"), # DataTable
    Output(component_id="detail-grid-container", component_property="rowData"), # AgGrid

    # corresponds to the rows as displayed by the Grid through filtering and sorting.    
    Input(component_id="pivot-table-container", component_property="rowData"),  
    # corresponds to the rows as displayed by the Grid through filtering and sorting.    
    Input(component_id="pivot-table-container", component_property="virtualRowData"),  
    Input(component_id="pivot-table-container", component_property="selectedRows"),
    Input(component_id="pivot-table-container", component_property="cellClicked"),
)
def update_detail_table(rowData, virtualRowData, selectedRows, cellClicked):
    if selectedRows:         
        # Sample filtering logic based on pivot table selection (modify as needed)
        # print(selected)
        # print(rows)
        # selected_cols = [x['name'] for x in df['cols']]
        # selected_col = selectedRows[0]['Store']
        # selected_rows = [x['name'] for x in df['rows']]
        selected_row = selectedRows[0]  # noqa: F841
        # print(f'selectedRows: {selected_row}')
        # filtered_df = df[df[selected_cols].isin([selected_row['Store']])]
        
        filtered_df = df.query("Store == @selected_row['Store'] & Country == @selected_row['Country'] & Cat == @selected_row['Cat'] ")
        # print(filtered_df)
        # return selectedRows 
        return filtered_df.to_dict("records")
    elif cellClicked and cellClicked['colId'] == 'ag-Grid-AutoColumn':
        # print(f'cellClicked {cellClicked}')
        filtered_df = df[df["Store"].isin([cellClicked['value']])]
        return filtered_df.to_dict("records")
        


@callback(
    Output("pivot-table-container", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    error_message = None
    df = None
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif filename in ['xls', 'xlsx']:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            error_message = 'Unsupported filetype'
    except Exception as e:
        print(e)        
        return html.Div([
            error_message or 'There was an error processing this file.'
        ])

    if df is not None and not df.empty:
        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr(),  # horizontal line

            # For debugging, display the raw contents provided by the web browser
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'), # State allows you to pass along extra values without firing the callbacks
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_text_output(n_clicks, input1, input2):
    return f'''
        The Button has been pressed {n_clicks} times,
        Input 1 is "{input1}",
        and Input 2 is "{input2}"
    '''
    
@callback(
    Output('boolean-switch-result', 'children'),
    Input('our-boolean-switch', 'on')
)
def update_switch_output(on):
    return f'The switch is {on}.'
    
if __name__ == "__main__":
    app.run_server(debug=True, # all of the Dev Tools features listed below enabled.
                   host='127.0.0.1', 
                   port='8050',
                   dev_tools_ui=True)
