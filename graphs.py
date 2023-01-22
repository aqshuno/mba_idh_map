import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as fig_factory
import pandas as pd
import numpy as np
import tsne as tsne
import transformations as trafo

region_code = {
    'Africa': 1,
    'Americas': 2,
    'Asia': 3,
    'Europe': 4,
    'Oceania': 5
}

def filterDataFrame(dfData, country, yearInterval):
    country_list = []
    if type(country) == str:
        country_list.append(country)
    else:
        country_list = country
    
    mask = (
        (dfData.year >= yearInterval[0])
        & (dfData.year <= yearInterval[1])
    )

    filtered_data = dfData.loc[mask, :]
    filtered_data = filtered_data[filtered_data.Country_name.isin(country_list)]

    return filtered_data

def update_lineChart(dfData, country, metric, yearInterval, width, height):  
    filtered_data = filterDataFrame(dfData, country, yearInterval)
    
    #df_filtered = df[df.country.isin(country_list)]
    fig = px.line(filtered_data, x="year", y=metric, color='Country_name')
    #fig.update_layout({'paper_bgcolor' : 'rgba(0, 0, 0, 0)', 'plot_bgcolor' : 'rgba(0, 0, 0, 0)'})
    #fig.update_xaxes(showline=True, linewidth=1, gridcolor='PapayaWhip')
    #fig.update_yaxes(showline=True, linewidth=1, gridcolor='PapayaWhip')

    fig.update_layout(
        #yaxis_title= metric,
        height=int(height * 0.63),
        width=int(width * 0.65),
        margin=dict(
            #l=120,  # left margin
            r=120,  # right margin
            b=0,  # bottom margin
            t=0,  # top margin
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )

    return fig

def update_correlation(dfData, country, metric, yearInterval, width, height):  
    filtered_data = filterDataFrame(dfData, country, yearInterval)

    metric_list = []
    if type(metric) == str:
        metric_list.append(metric)
    else:
        metric_list = metric
    
    if not metric_list:
        return {},
    
    df = pd.DataFrame(filtered_data, columns = metric_list)
    df_corr = df.corr()
    mask = np.triu(np.ones_like(df_corr, dtype=bool))
    df_mask = df_corr.mask(mask)
    
    x = list(df_corr.columns)
    y = list(df_corr.index)
    z = np.array(df_corr)
    
    fig_correlation = fig_factory.create_annotated_heatmap(
        z,
        x = x,
        y = y ,
        annotation_text = np.around(z, decimals=2),
        hoverinfo='z',
        colorscale=px.colors.diverging.Earth,
        showscale=True, ygap=1, xgap=1
    )
    
    fig_correlation.update_xaxes(side="bottom")
    
    fig_correlation.update_layout(
        title_text='Heatmap', 
        title_x=0.5, 
        height=int(height * 0.63),
        width=int(width * 0.65),
        margin=dict(
                #l=120,  # left margin
                r=120,  # right margin
                b=0,  # bottom margin
                t=0,  # top margin
        ),
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis_autorange='reversed',
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )
    
    for i in range(len(fig_correlation.layout.annotations)):
        if fig_correlation.layout.annotations[i].text == 'nan':
            fig_correlation.layout.annotations[i].text = ""
    
    return fig_correlation

def update_scatterplot(dfData, country, metric, yearInterval, width, height):  
    filtered_data = filterDataFrame(dfData, country, yearInterval)

    metric_list = []
    if type(metric) == str:
        metric_list.append(metric)
    else:
        metric_list = metric
    
    if not metric_list:
        return {},
    
    fig_scatterplot = px.scatter_matrix(
        filtered_data,
        dimensions = metric_list,
        color = 'Country_name',
        symbol= 'Country_name',
        title="Scatter matrix",
        height=int(height * 0.63),
        width=int(width * 0.65),
        labels={col:col.replace('_', ' ') for col in filtered_data.columns}, # remove underscore
    )
    fig_scatterplot.update_traces(diagonal_visible=True)
    fig_scatterplot.update_layout(
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )
    
    return fig_scatterplot

def update_bubble(dfData, country, metric, yearInterval, width, height):  
    filtered_data = filterDataFrame(dfData, country, yearInterval)

    metric_list = []
    if type(metric) == str:
        metric_list.append(metric)
    else:
        metric_list = metric

    print('Bubble - metrics: ', metric_list)
    
    if not metric_list:
        return {},
    
    if len(metric_list) < 2:
        return update_empty(width, height)

    
    filtered_df = filtered_data[filtered_data.year == yearInterval[1]]

    fig = px.scatter(filtered_df, x=metric_list[0], y=metric_list[1],
                        size='Total Population', color='Country_name', size_max=100)

    fig.update_layout(
        transition_duration=500,
        height=int(height * 0.63),
        width=int(width * 0.65),
    ),
    #fig.update_xaxes(visible=False, showticklabels=False),
    #fig.layout.plot_bgcolor = 'white'
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )
    return fig

# radar plot to compare index values
# --------------------------------------------------------------------------------------------------------------------------------------------------------#
def update_radar(data, city):
    # creating a subset dataframe
    df = data[
        [
            "Country_name",
            "Human Development Index",
            "Education Index",
            "Income Index",
            "Life Expectancy",
            "Gender Inequality Index",
        ]
    ]

    # categories
    cat = df.columns[1:].tolist()

    select_df = df[df["Country_name"] == city]

    Row_list = []
    r = []
    # Iterate over each row
    for index, rows in select_df.iterrows():
        for i in range(len(cat)):
            # Create list for the current
            r.append(rows[cat[i]])

            # append the list to the final list
        Row_list.append(r)
        Row_list = list(np.concatenate(Row_list).flat)

    fig = go.Figure()

    fig.add_trace(
        go.Barpolar(
            r=Row_list,
            theta=cat,
            name=city,
            marker_color=["rgb(243,203,70)"] * 6,
            marker_line_color="white",
            hoverinfo=["theta"] * 9,
            opacity=0.7,
            base=0,
        )
    )

    fig.add_trace(
        go.Barpolar(
            r=df.mean(axis=0).tolist(),
            theta=cat,
            name="Average",
            marker_color=["#986EA8"] * 6,
            marker_line_color="white",
            hoverinfo=["theta"] * 9,
            opacity=0.7,
            base=0,
        )
    )

    fig.update_layout(
        title="",
        font_size=12,
        margin=dict(
            l=110,  # left margin
            r=120,  # right margin
            b=0,  # bottom margin
            t=0,  # top margin
        ),
        height=150,
        width=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        legend=dict(orientation="h",),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(linewidth=3, showline=False, showticklabels=True),
            radialaxis=dict(
                showline=False,
                showticklabels=False,
                linewidth=2,
                gridcolor="rgba(0,0,0,0)",
                gridwidth=2,
            ),
        ),
    )

    return fig

def update_projection(dfData, country, metric, yearInterval, width, height):

    #filtered_data = filterDataFrame(dfData, country, yearInterval)

    #filtered_df = filtered_data[filtered_data.year == yearInterval[1]]
    #df_columns = filtered_df.drop(columns=['Country_code', 'Country_name', 'year'])
    #df_columns = filtered_df.drop(columns=['Country_code', 'year'])
    #df_columns = df_columns.dropna()
    #df_region = df_columns['Region']
    #df_country = df_columns['Country_name']
    #df_columns = df_columns.drop(columns=['Region'])
    #df_columns = df_columns.drop(columns=['Country_name'])
    #df_country.to_csv("labels_country.txt", header=None, index=None, sep=' ', mode='w')

    #print(df_columns.to_string())
    # Saving in file
    #df_columns.to_csv("foo.txt", header=None, index=None, sep=' ', mode='w')
    #df_region.to_csv("labels_region.txt", header=None, index=None, sep=' ', mode='w')
    #X = df_columns.to_numpy()
    #X = X[~np.isnan(X).any(axis=1)]

    X = np.loadtxt("foo.txt")
    X = trafo.unit_vector(X, axis=1)

    region_file = pd.read_csv("labels_region.txt", names=['region'])
    country_file = pd.read_csv("labels_country.txt", names=['country'])
    code = [region_code[region] for region in region_file['region']]

    #input("Press Enter to continue...")
    #X.tofile('foo.csv',sep=',',format='%10.5f')
    #labels = np.loadtxt("mnist2500_labels.txt")
    Y = tsne.tsne(X, 2, 10, 20.0)
    #pylab.scatter(Y[:, 0], Y[:, 1], 20, labels)
    #pylab.show()
    #print('____________________________________')
    #print('Y: ', type(Y))

    projection_data = pd.DataFrame(Y, columns = ['x', 'y'])
    projection_data['color'] = code
    projection_data['region'] = [region for region in region_file['region']]
    projection_data['country'] = [country for country in country_file['country']]

    fig = px.scatter(projection_data, x='x', y='y', color='region', hover_name='country', text='country')

    fig.update_layout(
        transition_duration=500,
        height=int(height * 0.63),
        width=int(width * 0.65),
    ),
    hover_name = [country for country in country_file['country']]
    fig.update_traces(mode="markers", hovertemplate="%{text}"),
    fig.update_xaxes(visible=False, showticklabels=False),
    fig.update_yaxes(visible=False, showticklabels=False),
    #fig.layout.plot_bgcolor = 'white'
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )
    return fig

def update_empty(width, height):

    fig = px.scatter()

    fig.update_layout(
        transition_duration=500,
        height=int(height * 0.63),
        width=int(width * 0.65),
    ),
    fig.update_xaxes(visible=False, showticklabels=False),
    fig.update_yaxes(visible=False, showticklabels=False),
    #fig.layout.plot_bgcolor = 'white'
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open sans", size=12, color="White"),
    )
    return fig