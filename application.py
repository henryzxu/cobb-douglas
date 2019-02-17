import dash
import dash_core_components as dcc
import dash_html_components as html
from gen_data import Properties, Change_Request, produce_data
import plotly.graph_objs as go
from plotly import tools
import pandas as pd
from dash.dependencies import Output, Input, State


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.layout = html.Div(children=[
    html.H1(children="Interactive Cobb-Douglas Production Function"),
    dcc.Graph(
        id='main-display'
    ),
    html.Div(children=[
    html.Div(id="current-graph-time", children="Current Time"),
    dcc.Slider(
        id='graph-time-slider',
        min=0,
        max=100,
        value=25,
        step=1
    ),
    html.Br(),
    html.H3(children="Basics"),
    html.Div(id="alpha", children="alpha"),
    dcc.Slider(
        id='alpha-slider',
        min=0.01,
        max=.99,
        value=.33,
        step=0.01
    ),
    html.Div(id="base-efficiency", children="base efficiency"),
    dcc.Slider(
        id='e-slider',
        min=0,
        max=10000,
        value=1000,
        step=100
    ),
    html.Div(id="efficiency-growth", children="efficiency growth"),
    dcc.Slider(
        id='g-slider',
        min=0.00,
        max=.5,
        value=.02,
        step=0.001
    ),
    html.Div(id="labor-growth", children="labor growth"),
    dcc.Slider(
        id='n-slider',
        min=0.00,
        max=.5,
        value=.02,
        step=0.001
    ),
    html.Div(id="savings", children="savings"),
    dcc.Slider(
        id='s-slider',
        min=0.00,
        max=.8,
        value=.2,
        step=0.001
    ),
    html.Div(id="depreciation", children="depreciation"),
    dcc.Slider(
        id='d-slider',
        min=0.00,
        max=.5,
        value=.05,
        step=0.001
    ),
    html.Br(),
    html.H3(children="Experimental (may not update correctly)"),
    html.Div(id="delta-g", children="delta g"),
    dcc.Slider(
        id='delta-g-slider',
        min=0.00,
        max=.1,
        value=0,
        step=0.001
    ),
html.Div(id="delta-n", children="delta n"),
    dcc.Slider(
        id='delta-n-slider',
        min=0.00,
        max=.1,
        value=0,
        step=0.001
    ),
html.Div(id="delta-s", children="delta s"),
    dcc.Slider(
        id='delta-s-slider',
        min=0.00,
        max=.1,
        value=0,
        step=0.001
    ),
html.Div(id="delta-d", children="delta d"),
    dcc.Slider(
        id='delta-d-slider',
        min=0.00,
        max=.1,
        value=0,
        step=0.001
    ),
    html.Br(),
    html.H3(children="Other"),
    html.Div(id="n-periods", children="number of time periods"),
    dcc.Slider(
        id='time-slider',
        min=0,
        max=100,
        value=25,
        step=1
    ),
        html.Br(),
        html.Div(id="change-request", children="Dynamic Change Requests"),

    dcc.Input(id='request-change', type='text', placeholder='<time period> <parameter> <new val>, <time period> <parameter> <new val>',
              style={'width': '50%'}),
    html.Div(id='change-request-list', children='Example: 10 n 0.06, 20 g 0.1'),
    html.Div(id='data-value', style={'display': 'none'})], style={'margin': 100})], style={'margin':50, 'textAlign': 'center'})

default_p = Properties(.33, 1000, 0.02, 0.02, 0.2, 0.05)
default_df, _ = produce_data(default_p, 100, [])

@app.callback(Output('n-periods', 'children'),
              [dash.dependencies.Input('time-slider', 'value')])
def update_time_slider(t):
     return '''Number of Time Periods: {}'''.format(t)

@app.callback(Output('delta-d', 'children'),
              [dash.dependencies.Input('delta-d-slider', 'value')])
def update_time_slider(t):
     return '''delta d: {}'''.format(t)

@app.callback(Output('delta-s', 'children'),
              [dash.dependencies.Input('delta-s-slider', 'value')])
def update_time_slider(t):
     return '''delta s: {}'''.format(t)

@app.callback(Output('delta-n', 'children'),
              [dash.dependencies.Input('delta-n-slider', 'value')])
def update_time_slider(t):
     return '''delta n: {}'''.format(t)

@app.callback(Output('delta-g', 'children'),
              [dash.dependencies.Input('delta-g-slider', 'value')])
def update_time_slider(t):
     return '''delta g: {}'''.format(t)

@app.callback(Output('depreciation', 'children'),
              [dash.dependencies.Input('d-slider', 'value')])
def update_time_slider(t):
     return '''Depreciation (d): {}'''.format(t)

@app.callback(Output('savings', 'children'),
              [dash.dependencies.Input('s-slider', 'value')])
def update_time_slider(t):
     return '''Savings (s): {}'''.format(t)

@app.callback(Output('labor-growth', 'children'),
              [dash.dependencies.Input('n-slider', 'value')])
def update_time_slider(t):
     return '''Labor Growth (n): {}'''.format(t)

@app.callback(Output('base-efficiency', 'children'),
              [dash.dependencies.Input('e-slider', 'value')])
def update_time_slider(t):
     return '''Base Efficiency (E): {}'''.format(t)

@app.callback(Output('alpha', 'children'),
              [dash.dependencies.Input('alpha-slider', 'value')])
def update_time_slider(t):
     return '''alpha: {}'''.format(t)

@app.callback(Output('efficiency-growth', 'children'),
              [dash.dependencies.Input('g-slider', 'value')])
def update_time_slider(t):
     return '''Efficiency Growth (g): {}'''.format(t)

@app.callback(Output('current-graph-time', 'children'),
              [dash.dependencies.Input('graph-time-slider', 'value')])
def update_time_slider(t):
     return '''Current Time: {}'''.format(t)



def parse_requests(s):
    try:
        if "format" in s:
            return []
        s = s.strip()
        ret = []
        s = s.split(",")
        for c in s:
            if c:
                c = c.strip().split(" ")
                ret.append(Change_Request(int(c[0]), c[1], float(c[2])))
        return ret
    except:
        return []

@app.callback(Output('data-value', 'children'), [dash.dependencies.Input('alpha-slider', 'value'),
     dash.dependencies.Input('n-slider', 'value'),
     dash.dependencies.Input('g-slider', 'value'),
     dash.dependencies.Input('s-slider', 'value'),
     dash.dependencies.Input('e-slider', 'value'),
     dash.dependencies.Input('d-slider', 'value'),
     dash.dependencies.Input('delta-n-slider', 'value'),
     dash.dependencies.Input('delta-g-slider', 'value'),
     dash.dependencies.Input('delta-s-slider', 'value'),
     dash.dependencies.Input('delta-d-slider', 'value'),
     dash.dependencies.Input('time-slider', 'value'),
     Input('request-change', 'value')])
def gen_data(alpha, n, g, s, e, d, delta_n, delta_g, delta_s, delta_d, time, changes):
     p = Properties(alpha, e, g, n, s, d, delta_g, delta_n, delta_d, delta_s)
     df, _ = produce_data(p, time, parse_requests(changes))
     return df.to_json(orient='split')


@app.callback(Output('change-request-list', 'children'), [
     Input('request-change', 'value')])
def update_requests(changes):
    changes_requested = parse_requests(changes)

    if len(changes_requested) == 0:
        return 'Example: 10 n 0.06, 20 g 0.1'
    formatted_requests = []
    for index, e in enumerate(changes_requested):
        formatted_requests.append(html.Div(children="{}: {}".format(index, str(e))))

    return formatted_requests

@app.callback(Output('graph-time-slider', 'max'),
              [dash.dependencies.Input('time-slider', 'value')])
def update_graph_slider(t):
     return t

@app.callback(
    dash.dependencies.Output('main-display', 'figure'),
    [Input('data-value', 'children'),
     Input('graph-time-slider', 'value')]
)
def update_figure(data, curr_time):
    df = pd.read_json(data, orient='split')
    fig = tools.make_subplots(rows=2, cols=3,
                              specs=[[{"colspan": 3}, None, None],
                                 [{}, {}, {}]],
                              subplot_titles=('Main Production Function', 'g(Y/L) over Time',
                                              'g(K/L) over Time', 'Y/L over Time')
                              )
    for i in range(curr_time):
        fig.append_trace(go.Scatter(
            x=df["k_over_l"][i],
            y=df["y_over_l"][i],
            mode='lines',
            opacity=0.7,
            legendgroup='group1',
            name="t={}, E={:n}".format(i, int(df["metadata"][i]["e"])),
            showlegend=False
        ), 1, 1)
    fig.append_trace(go.Scatter(
        x=df["point_k_over_l"][:curr_time],
        y=df["point_y_over_l"][:curr_time],
        mode='lines+markers',
        opacity=0.7,
        legendgroup='group4',
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name="Point Starting at BGE"
    ), 1, 1)
    fig.append_trace(go.Scatter(
        x=df["bge_k_over_l"][:curr_time],
        y=df["bge"][:curr_time],
        mode='lines+markers',
        opacity=0.7,
        legendgroup='group5',
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name="BGE"
    ), 1, 1)
    fig.append_trace(go.Scatter(
        x=[0] + default_df["bge_k_over_l"][:curr_time],
        y=[0] + default_df["bge"][:curr_time],
        mode='lines+markers',
        opacity=0.7,
        legendgroup='group2',
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name="Original BGE"
    ), 1, 1)
    fig.append_trace(go.Scatter(
            x=df["t"][1:curr_time],
            y=df["change_in_y_over_l"][1:curr_time],
            mode='lines',
            opacity=0.7,
        legendgroup='group4',
        name="Point g(Y/L)"
        ), 2, 1)
    fig.append_trace(go.Scatter(
        x=df["t"][1:curr_time],
        y=df["change_in_bge_y_over_l"][1:curr_time],
        mode='lines',
        opacity=0.7,
        legendgroup='group5',
        name="BGE g(Y/L)"
    ), 2, 1)

    fig.append_trace(go.Scatter(
        x=df["t"][1:curr_time],
        y=df["change_in_k_over_l"][1:curr_time],
        mode='lines',
        opacity=0.7,
        legendgroup='group4',
        name="Point g(K/L)"
    ), 2, 2)
    fig.append_trace(go.Scatter(
        x=df["t"][1:curr_time],
        y=df["change_in_bge_k_over_l"][1:curr_time],
        mode='lines',
        opacity=0.7,
        legendgroup='group5',
        name="BGE g(K/L)"
    ), 2, 2)
    fig.append_trace(go.Scatter(
        x=df["t"][:curr_time],
        y=df["bge"][:curr_time],
        mode='lines',
        opacity=0.7,
        legendgroup='group4',
        name="BGE Y/L w.r.t T"
    ), 2, 3)
    fig.append_trace(go.Scatter(
        x=df["t"][:curr_time],
        y=df["point_y_over_l"][:curr_time],
        mode='lines',
        opacity=0.7,
        legendgroup='group5',
        name="Point Y/L w.r.t T"
    ), 2, 3)


    fig['layout'].update(height=900, hovermode='closest',
                yaxis={
                             'range': [min(df["bge"][:curr_time].min(), df["point_y_over_l"][:curr_time].min()) * 0.3, max(df["bge"][:curr_time].max(),
                                                                                                   df["point_y_over_l"][:curr_time].max()) * 1.15]
                         },

                         xaxis={
                             'range': [min(df["bge_k_over_l"][:curr_time].min(), df["point_k_over_l"][:curr_time].min()) * 0.3,
                                       max(df["bge_k_over_l"][:curr_time].max(),
                                                                                                   df[
                                                                                                       "point_k_over_l"][:curr_time].max()) * 1.15]
                         },

                         )
    fig['layout']['xaxis1'].update(title='K/L')
    fig['layout']['xaxis2'].update(title='t')
    fig['layout']['xaxis3'].update(title='t')
    fig['layout']['xaxis4'].update(title='t')

    fig['layout']['yaxis1'].update(title='Y/L')
    min_x = min(df["change_in_bge_y_over_l"].min(), df["change_in_y_over_l"].min())
    max_x = max(df["change_in_bge_y_over_l"].max(), df["change_in_y_over_l"].max())
    pos_clamp = lambda x: x * 1.5 if x > 0 else x * 1.5
    neg_clamp = lambda x: x * -1.5 if x > 0 else x * -1.5
    fig['layout']['yaxis2'].update(title='g(Y/L)')
    min_x = min(df["change_in_bge_k_over_l"].min(), df["change_in_k_over_l"].min())
    max_x = max(df["change_in_bge_k_over_l"].max(), df["change_in_k_over_l"].max())
    fig['layout']['yaxis3'].update(title='g(K/L)')
    fig['layout']['yaxis4'].update(title='Y/L')

    return fig





if __name__ == '__main__':
    application.run(debug=True)