import dash
from dash import dcc, ctx
from dash import html
from dash.dependencies import Output, Input,  ClientsideFunction, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import graphs as gph
import tabs as tbs

import json
import time

data_countries = pd.read_csv("data2.csv")

minYear = min(data_countries.year)
maxYear = max(data_countries.year)

region_code = {
    'Africa' : 0,
    'Americas' : 0.15,
    'Antarctica' : 0.30,
    'Asia' : 0.45,
    'Europe' : 0.60,
    'Oceania' : 0.75
}

metrics = ['Life Expectancy','Human Development Index','Education Index','Income Index','Gross National Income',
'Total Population','Gender Inequality Index','Unemployment','Life Expectancy',
'Mean Years of Schooling']

countries = [country for country in np.sort(data_countries.Country_name.unique())]

def scale_size(X, old_min, old_max, new_min=0, new_max=1):
    new_scale = new_max - ((new_max - new_min) * (old_max - X) / (old_max - old_min))

    return 100 if new_scale > 100 else new_scale

#selected_location = ""
x_close_selection_clicks = -1
hovered_location = ""
projecting = False

filter_list = ['high beer','low beer','high festival','low festival','high avgtemperature']

app = dash.Dash(__name__)

filters_layout = html.Div(
    [
        html.Div(
            [
                html.H3("Parameters", style={"display": "inline"}),
                html.Span(
                    [html.Span(className="Select-arrow", title="is_open")],
                    className="Select-arrow-zone",
                    id="select_filters_arrow",
                ),
            ],
        ),
        html.Div(
            [
                html.P("Metric:", id="preferencesText"),
                dcc.Dropdown(
                    placeholder="Select ...",
                    id="filters_drop",
                    options=metrics,
                    value=metrics[0],
                    clearable=True,
                    className="dropdownMenu",
                    multi=False,
                ),
                html.P("Countries:", id="countriesText"),
                dcc.Dropdown(
                    placeholder="Select ...",
                    id="filters_countries",
                    options=countries,
                    clearable=True,
                    className="dropdownMenu",
                    multi=True,
                ),
            ],
            id="dropdown_menu_applied_filters",
        ),
    ],
    id="filters_container",
    style={"display": "block"}, #"position": "absolute", "top":"100px"
    className="stack-top col-3",
)

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'color':'#586069',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'border-top': '3px solid transparent',
    'border-left': '0px',
    'border-right': '0px',
    'border-bottom': '0px',
    'background-color': '#333333',
    'padding': '12px',
    'font-family': 'system-ui',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#333333',
    'color': 'white',
    'padding': '6px'
}

selected_location_layout = html.Div(
    [
        html.Div(
            [
                html.H3("Information", id="title_selected_location"),
                html.Span("X", id="x_close_selection"),
            ]
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [
        #                 html.H4("... Common indices and Quartiles analysis"),
        #                 html.H6(
        #                     "Bubble size is GDP per capita. Brush to highlight cities."
        #                 ),
        #                 dcc.Graph(id="bubble"),
        #             ],
        #             className="plot_container_child",
        #         ),
        #         html.Div(
        #             [
        #                 html.H4("... Selected preferences"),
        #                 dcc.Graph(id="custom_dims_plot"),
        #             ],
        #             className="plot_container_child",
        #         ),
        #     ],
        #     className="plots_container",
        # ),
        html.Div(
            [
                #dcc.Graph(id="lineChart_plot"),
                dcc.Tabs(
                    id="tabs-with-classes",
                    value='tab-lineChart',
                    parent_className='custom-tabs',
                    #className='custom-tabs-container',
                    children = [
                        dcc.Tab(
                            label='Line Chart',
                            value='tab-lineChart',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            className='custom-tab',
                            selected_className='custom-tab-selected',
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="lineChart_plot", config={"displayModeBar": False},
                                    ),
                                    className="cardWrapper",
                                ),
                            ],
                            #style={"background-color": "red"},
                            #className="wrapper",
                        ),
                        dcc.Tab(
                            label='Correlation',
                            value='tab-correlation',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            className='custom-tab',
                            selected_className='custom-tab-selected',
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="correlation_plot", config={"displayModeBar": False},
                                    ),
                                    className="cardWrapper",
                                ),
                            ],
                            #className="wrapper",
                        ),
                        dcc.Tab(
                            label='Scatter Matrix',
                            value='tab-scatterplot',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            className='custom-tab',
                            selected_className='custom-tab-selected',
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="scatterplot", config={"displayModeBar": False},
                                    ),
                                    className="cardWrapper",
                                ),
                            ],
                            #className="wrapper",
                        ),
                        dcc.Tab(
                            label='Bubble Chart',
                            value='tab-bubble',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            className='custom-tab',
                            selected_className='custom-tab-selected',
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="bubble_chart",
                                        config={
                                            'staticPlot': False,     # True, False
                                            'scrollZoom': False,      # True, False
                                            'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                                            'showTips': True,       # True, False
                                            'displayModeBar': 'hover',  # True, False, 'hover'
                                            'watermark': False,
                                            'modeBarButtonsToRemove': ['pan2d','select2d', 'lasso2d', 'autoScale2d', 'resetScale2d', 'zoom2d']
                                        },
                                    ),
                                    className="cardWrapper",
                                ),
                            ],
                            #className="wrapper",
                        ),
                        dcc.Tab(
                            label='Projection',
                            value='tab-projection',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            className='custom-tab',
                            selected_className='custom-tab-selected',
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="projection_chart",
                                    ),
                                    className="cardWrapper",
                                ),
                                html.Div([
                                    html.Button('Calculate', id='button-projection', n_clicks=0),
                                    dcc.Loading(
                                        id="loading",
                                        children=[html.Div([html.Div(id="loading-output")])],
                                        type="circle",
                                        fullscreen=False,
                                    )
                                ])
                            ],
                            #className="wrapper",
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            dcc.RangeSlider(minYear, maxYear, 1, value=[minYear, maxYear], id='year-slider', tooltip={"placement": "bottom", "always_visible": True},
                marks ={
                    1990: '1990',
                    1995: '1995',
                    2000: '2000',
                    2005: '2005',
                    2010: '2010',
                    2015: '2015'
                }
            ),
            style={"width": "1300px", "margin-left": "auto", "margin-right": "auto", "align-items": "center"},
            #className="plot_container_child",
        )
    ],
    id="selected_location",
    style={"display": "none"},
)

hovered_location_layout = html.Div(
    [
        html.Div([
            html.H3("city", id="hover_title"),
            dcc.Graph("radar")
        ]),
    ],
    id="hovered_location",
    style={"display": "none"},
)

# APP layout
# --------------------------------------------------------------------------------------------------------------------------------------------------------#
app.layout = html.Div(
    children=[
        # html.H1(children="Avocado Analytics",),
        # html.P(
        #     children="Analyze the behavior of avocado prices"
        #     " and the number of avocados sold in the US"
        #     " between 2015 and 2018",
        # ),
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                html.Div(
                    id="width", style={"display": "none"}
                ),  # Just to retrieve the width of the window
                html.Div(
                    id="height", style={"display": "none"}
                ),  # Just to retrieve the height of the window
                html.Div(
                    [
                        dcc.Graph(
                            id="map",
                            clear_on_unhover=True,
                            config={"doubleClick": "reset"},
                        )
                    ],
                    style={"width": "100%", "height": "100%"},
                    className="background-map-container",
                ),
                filters_layout,
            ],
            id="map_container",
            style={"display": "flex"},
        ),
        selected_location_layout,
        hovered_location_layout,
    ],
    id="page-content",
    style={"position": "relative"},
)



# End of layout
# --------------------------------------------------------------------------------------------------------------------------------------------------------#




# --------------------------------------------------------------------------------------------------------------------------------------------------------#
# Connect the Plotly graphs with Dash Components



@app.callback(
    Output("dropdown_menu_applied_filters", "style"),
    Output("select_filters_arrow", "title"),
    Input("select_filters_arrow", "n_clicks"),
    State("select_filters_arrow", "title"),
)
def toggle_applied_filters(n_clicks, state):
    style = {"display": "none"}
    if n_clicks is not None:
        if state == "is_open":
            style = {"display": "none"}
            state = "is_closed"
        else:
            style = {"display": "block"}
            state = "is_open"

    return style, state

@app.callback(
    [
        Output("selected_location", "style"),
        #Output("title_selected_location", "children"),
        #Output("custom_dims_plot", "figure"),
        #Output("bubble", "figure"),
        Output("filters_drop", "value"),
        Output('filters_countries', 'value'),
        Output("lineChart_plot", "figure"),
        Output("correlation_plot", "figure"),
        Output("scatterplot", "figure"),
        Output("bubble_chart", "figure"),
        Output("projection_chart", "figure"),
    ],
    [
        Input("map", "clickData"),
        Input("x_close_selection", "n_clicks"),
        Input("filters_drop", "value"),
        Input('filters_countries', 'value'),
        Input("map", "selectedData"),
        #Input("bubble", "selectedData"),
        #Input("bubble", "clickData"),
        Input("width", "n_clicks"),
        Input("height", "n_clicks"),
        #State("bubble", "figure"),
        Input("year-slider", "value"),
        Input('button-projection', 'n_clicks'),
    ]
)
def update_selected_location(
    clickData,
    n_clicks,
    filters_metrics,
    filters_countries,
    mapSelect,
    #bubbleSelect,
    #bubbleClick,
    width,
    height,
    #bubbleState,
    yearInterval,
    button_projection_clicks
):

    print("############################################################### Start")
    #global selected_location
    global x_close_selection_clicks
    location = ""
    style = {"display": "none"}
    selected_countries = [] if filters_countries is None else filters_countries
    selected_metrics = metrics[0] if filters_metrics is None else filters_metrics
    triggered = ctx.triggered[0]['prop_id']
    projection = None
    global projecting

    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)

    #print(ctx_msg)


    if clickData is not None:
        print("*** Entrei clicked")
        print('++++++++++ Triggou: ',  triggered)

        print("Equal? ", triggered == 'map.clickData')

        if triggered == 'map.selectedData':
            if mapSelect is not None:
                print("*** Entrei lasso")
                selected_countries = [point['text'] for point in mapSelect['points']]
                style = {"display": "block"}
            elif clickData is not None:
                print("*** One Click")
                location = clickData["points"][0]["text"]

                if len(location) != 0:
                    print("*** There is a country")
                    selected_countries.append(location)
                    style = {"display": "block"}
        elif triggered == 'map.clickData':
            if clickData is not None:
                print("*** One Click")
                location = clickData["points"][0]["text"]

                if len(location) != 0:
                    print("*** There is a country")
                    selected_countries.append(location)
                    style = {"display": "block"}
        elif triggered == 'filters_countries.value':
            if filters_metrics is not None and filters_countries is not None and len(filters_countries) !=0:
                print("*** Entrei countries")
                selected_countries = filters_countries
                style = {"display": "block"}
        elif triggered == 'filters_drop.value':
            if filters_countries is not None and filters_metrics is not None and len(filters_metrics) !=0:
                print("*** Entrei metrics")
                selected_metrics = filters_metrics
                style = {"display": "block"}
        elif triggered == 'x_close_selection.n_clicks':
            print("-- Closing panel")
            style = {"display": "none"}
        elif triggered == 'year-slider.value':
            print("-- Changing year range")
            style = {"display": "block"}
        else:
            print("*** Nada de pitibiriga")
            style = {"display": "none"}
        
        if triggered == 'button-projection.n_clicks':
            projection = gph.update_projection(data_countries, selected_countries, selected_metrics, yearInterval, width, height)
            projecting = False
            style = {"display": "block"}
        else:
            projection = gph.update_empty(width, height)


    # if n_clicks != x_close_selection_clicks:
    #     print("-- Differenca de clicks")
    #     style = {"display": "none"}
    #     x_close_selection_clicks = n_clicks
        

    # if bubbleSelect is not None or bubbleClick is not None or bubbleState is not None:
    #     bubble_fig = update_color(bubbleSelect, bubbleClick, bubbleState, width, height)
    # else:
    #     bubble_fig = build_bubble_figure(width, height)
    return (
        style,
        #"Compare " + location + " with other cities using...",
        #update_custom_dims_plot(location, dims_selected, width, height),
        #bubble_fig,
        selected_metrics,
        selected_countries,
        gph.update_lineChart(data_countries, selected_countries, selected_metrics, yearInterval, width, height),
        gph.update_correlation(data_countries, selected_countries, selected_metrics, yearInterval, width, height),
        gph.update_scatterplot(data_countries, selected_countries, selected_metrics, yearInterval, width, height),
        gph.update_bubble(data_countries, selected_countries, selected_metrics, yearInterval, width, height),
        projection,
    )

@app.callback(Output("loading-output", "children"), Input('button-projection', 'n_clicks'))
def input_triggers(value):
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK ", value)
    global projecting

    if value != 0:
        projecting = True
        while(projecting):
            time.sleep(1)
        
        #return value

@app.callback(
    [
        Output("hovered_location", "style"),
        Output("radar", "figure"),
        Output("hover_title", "children"),
    ],
    [
        Input("map", "hoverData")
    ],
)
def update_hovered_location(hoverData):
    global hovered_location
    location = ""
    if hoverData is not None:
        location = hoverData["points"][0]["text"]
        if location != hovered_location:
            hovered_location = location
            style = {"display": "block"}
        else:
            hovered_location = ""
            location = ""
            style = {"display": "none"}
    else:
        hovered_location = ""
        location = ""
        style = {"display": "none"}

    return style, gph.update_radar(data_countries.loc[data_countries['year'] == 2019], location), location

@app.callback(
    Output("page-content", "style"),
    Input("width", "n_clicks"),
    Input("height", "n_clicks"),
)
def set_page_size(width, height):
    return {"width": width, "height": height}

def regionMapBox(data, region, color):
    highlighted = data.loc[data['Region'] == region]
    
    return go.Scattermapbox(
            lat=highlighted.Lat,
            lon=highlighted.Lon,
            text=highlighted.Country_name,
            name=region,
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=highlighted.sizeCircle, 
                color=color,
                opacity=0.9, 
                showscale=False
            ),
            hovertemplate="<extra></extra>",
    )

@app.callback(
    [Output("map", "figure")],
    [
        Input("width", "n_clicks"),
        Input("height", "n_clicks")
    ]
)
def update_map(width, height):
    fig = go.Figure()

    filtered = data_countries.loc[data_countries['year'] == 2019]
    filtered = filtered.drop_duplicates(['Country_name', 'Region', 'Total Population', 'Lat', 'Lon'])

    old_min = min(filtered['Total Population'])
    old_max = max(filtered['Total Population'])
    filtered['sizeCircle'] = [scale_size(population, old_min, old_max, new_min=10, new_max=300)  for population in filtered['Total Population']]

    # if filter_list is not None and len(filter_list) != 0:

    #     filters = []
    #     for f in filter_list:
    #         filters.append(data_countries[f])
    #     highlighted = data_countries.loc[
    #         np.all(filters, 0), ["City", "Country", "Lat", "Long"]
    #     ]
    #     not_highlighted = data_countries.loc[
    #         ~np.all(filters, 0), ["City", "Country", "Lat", "Long"]
    #     ]

    #     print("Highlighted: ", highlighted)

    #     # Highlighted
    #     fig.add_trace(
    #         go.Scattermapbox(
    #             lat=highlighted.Lat,
    #             lon=highlighted.Long,
    #             text=highlighted.City,
    #             name="Compatible location",
    #             mode="markers",
    #             marker=go.scattermapbox.Marker(size=15, opacity=0.9, color="#F3D576",),
    #             hovertemplate="<extra></extra>",
    #         )
    #     )
    # else:
    #     not_highlighted = data_countries

    # africa = regions.AFRICA
    # americas = regions.AMERICAS
    # antarctica = regions.ANTARCTICA
    # asia = regions.ASIA
    # europe = regions.EUROPE
    # oceania = regions.OCEANIA
    
    
    # Not highlighted
    fig.add_trace(regionMapBox(filtered, 'Africa', '#F3D576'))
    fig.add_trace(regionMapBox(filtered, 'Americas', '#0091D5'))
    #fig.add_trace(regionMapBox(filtered, 'Antartica', 'black'))
    fig.add_trace(regionMapBox(filtered, 'Asia', '#6AB187'))
    fig.add_trace(regionMapBox(filtered, 'Europe', '#AC3E31'))
    fig.add_trace(regionMapBox(filtered, 'Oceania', '#7E909A'))

    mapbox_token = "pk.eyJ1IjoiZmFya2l0ZXMiLCJhIjoiY2ttaHYwZnQzMGI0cDJvazVubzEzc2lncyJ9.fczsOA4Hfgdf8_bAAZkdYQ"
    all_plots_layout = dict(
        mapbox=dict(
            style="mapbox://styles/farkites/ckn0lwfm319ae17o5jmk3ckvu",
            accesstoken=mapbox_token,
        ),
        legend=dict(
            bgcolor="rgba(51,51,51,0.6)",
            yanchor="top",
            y=0.35,
            xanchor="left",
            x=0,
            font=dict(family="Open Sans", size=15, color="white",),
        ),
        autosize=False,
        width=width,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="lasso",
        hovermode="closest",
    )
    fig.layout = all_plots_layout

    return fig,


@app.callback(
    Output('filters_drop', 'multi'),
    Input('tabs-with-classes', 'value')
)
def render_content(tab):
    if tab == 'tab-lineChart':
        return False
    elif tab == 'tab-correlation':
        return True
    elif tab == 'tab-scatterplot':
        return True
    elif tab == 'tab-bubble':
        return True
    elif tab == 'tab-projection':
        return False

# Get window size function
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="get_window_width"),
    Output("width", "n_clicks"),
    [Input("url", "href")],
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="get_window_height"),
    Output("height", "n_clicks"),
    [Input("url", "href")],
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="move_hover"),
    Output("hovered_location", "title"),
    [Input("map", "hoverData")],
)

if __name__ == "__main__":
    app.run_server(debug=True)