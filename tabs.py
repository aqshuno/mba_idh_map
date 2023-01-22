from dash import dcc
from dash import html

tabs = dcc.Tabs(
    id="tabs-with-classes",
    value='tab-chart',
    parent_className='custom-tabs',
    className='custom-tabs-container',
    children = [
        dcc.Tab(
            label='Line Chart',
            value='tab-lineChart',
            className='custom-tab',
            selected_className='custom-tab--selected',
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="lineChart_plot", config={"displayModeBar": False},
                    ),
                    className="cardWrapper",
                ),
            ],
            #className="wrapper",
        ),
        dcc.Tab(
            label='Correlation',
            value='tab-correlation',
            className='custom-tab',
            selected_className='custom-tab--selected',
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
            className='custom-tab',
            selected_className='custom-tab--selected',
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
            className='custom-tab',
            selected_className='custom-tab--selected',
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
    ]
),

def myTabs():
    return tabs