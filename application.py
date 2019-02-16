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
    dcc.Graph(
        id='main-display'
    ),
    html.Div(children="alpha"),
    dcc.Slider(
        id='alpha-slider',
        min=0.01,
        max=.99,
        value=.33,
        step=0.01
    ),
    html.Div(children="base efficiency"),
    dcc.Slider(
        id='e-slider',
        min=0,
        max=10000,
        value=1000,
        step=100
    ),
    html.Div(children="efficiency growth"),
    dcc.Slider(
        id='g-slider',
        min=0.00,
        max=.5,
        value=.02,
        step=0.001
    ),
    html.Div(children="labor growth"),
    dcc.Slider(
        id='n-slider',
        min=0.00,
        max=.5,
        value=.02,
        step=0.001
    ),
    html.Div(children="savings"),
    dcc.Slider(
        id='s-slider',
        min=0.00,
        max=.8,
        value=.2,
        step=0.001
    ),
    html.Div(children="depreciation"),
    dcc.Slider(
        id='d-slider',
        min=0.00,
        max=.5,
        value=.05,
        step=0.001
    ),
    html.Div(children="Following 4 sliders are highly experimental"),
    dcc.Slider(
        id='delta-g-slider',
        min=0.00,
        max=.2,
        value=0,
        step=0.001
    ),
    dcc.Slider(
        id='delta-n-slider',
        min=0.00,
        max=.2,
        value=0,
        step=0.001
    ),
    dcc.Slider(
        id='delta-s-slider',
        min=0.00,
        max=.2,
        value=0,
        step=0.001
    ),
    dcc.Slider(
        id='delta-d-slider',
        min=0.00,
        max=.2,
        value=0,
        step=0.001
    ),
    html.Div(children="Keep number of time periods relatively low for fastest performance, high for better visualization of convergence"),
    html.Div(children="time periods"),
    dcc.Slider(
        id='time-slider',
        min=0,
        max=100,
        value=25,
        step=1
    ),
    dcc.Input(id='request-change', type='text', value='format: 10 n 0.02'),
    html.Div(id='data-value', style={'display': 'none'})
])



def parse_requests(s):
    if "format" in s:
        return []
    s = s.strip()
    ret = []
    try:
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

@app.callback(
    dash.dependencies.Output('main-display', 'figure'),
    [Input('data-value', 'children')]
)
def update_figure(data):
    df = pd.read_json(data, orient='split')
    fig = tools.make_subplots(rows=2, cols=3,
                              specs=[[{"colspan": 3}, None, None],
                                 [{}, {}, {}]])
    for i in df["t"]:
        fig.append_trace(go.Scatter(
            x=df["k_over_l"][i],
            y=df["y_over_l"][i],
            mode='lines',
            opacity=0.7,
            name=i
        ), 1, 1)
    fig.append_trace(go.Scatter(
        x=df["point_k_over_l"],
        y=df["point_y_over_l"],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
    ), 1, 1)
    fig.append_trace(go.Scatter(
        x=df["bge_k_over_l"],
        y=df["bge"],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
    ), 1, 1)
    fig.append_trace(go.Scatter(
            x=df["t"][1:],
            y=df["change_in_y_over_l"][1:],
            mode='lines',
            opacity=0.7,
        ), 2, 1)
    fig.append_trace(go.Scatter(
        x=df["t"][1:],
        y=df["change_in_k_over_l"][1:],
        mode='lines',
        opacity=0.7,
    ), 2, 2)
    fig.append_trace(go.Scatter(
        x=df["t"],
        y=df["bge"],
        mode='lines',
        opacity=0.7,
    ), 2, 3)


    fig['layout'].update(height=800, width=1000, hovermode='closest',
                yaxis={
                    'title': 'Y/L',
                             'range': [min(df["bge"]) * 0.3, max(df["bge"]) * 1.1]
                         },
                         )
    return fig


if __name__ == '__main__':
    application.run(debug=True)