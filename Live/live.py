import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
from sqlalchemy import create_engine

# import sqlite3
# import xlwt 

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

app = dash.Dash(__name__)

# Create a simple database
engine = create_engine('sqlite:///sample.db')

app.layout = html.Div(
    [

        html.H1("Live Data Streaming",
                style = {
                        'textAlign':'Center'

                }),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )
    df = pd.DataFrame({
    'x': list(X),
    'y': list(Y)
    })
    df.to_sql('dataframe', engine, if_exists='replace')

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}



  


if __name__ == '__main__':
    app.run_server(debug=True)