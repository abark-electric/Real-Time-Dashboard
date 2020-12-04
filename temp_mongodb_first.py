import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
from plotly import graph_objs
from collections import deque    # Define max size
import pymongo
import constants
import logging

client = pymongo.MongoClient(constants.MONGODB_CONN)
X = []
Y = []
X.append(1)
Y.append(1)
count = 0
resume_token = 'NEW'
token_holder = []
token_holderx = []

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000
    )
])


@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph():

    #print(resume_token)

    global token_holder
    global token_holderx
    find_dup(token_holderx)
    print(token_holderx)
    global X
    global Y
    global client
    global resume_token
    if resume_token is "NEW":
        with client.changestream.collection.watch() as stream:
            for insert_change in stream:

                resume_token = stream.resume_token

                # print('Working 3')
                # print(change['fullDocument']['hello'])

                # print('Working 4')
                print('')  # for readability only

                if resume_token not in token_holder:
                    X.append(X[-1] + 1)
                    Y.append(insert_change['fullDocument']['hello'])
                    # print(insert_change['fullDocument']['hello'])
                    # print(X)
                    # print(Y)


                    data = graph_objs.Scatter(
                        x=list(X),
                        y=list(Y),
                        name='Scatter',
                        mode='markers'
                    )
                    token_holder.append(resume_token)
                    token_holderx.append(resume_token['_data'])
                    return {'data': [data], 'layout': graph_objs.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                                        yaxis=dict(range=[min(Y), max(Y)]))}
    else:
        with client.changestream.collection.watch(resume_after=resume_token) as stream:
            for insert_change in stream:

                resume_token = stream.resume_token
                # token_holder.append(resume_token)
                # print('Working 3')
                # print(change['fullDocument']['hello'])

                # print('Working 4')
                # print('')  # for readability only
                if resume_token not in token_holder:
                    X.append(X[-1] + 1)
                    Y.append(insert_change['fullDocument']['hello'])
                    # print(insert_change['fullDocument']['hello'])
                    # print(X)
                    # print(Y)

                    data = graph_objs.Scatter(
                        x=list(X),
                        y=list(Y),
                        name='Scatter',
                        mode='markers'
                    )
                    token_holder.append(resume_token)
                    token_holderx.append(resume_token['_data'])
                    return {'data': [data], 'layout': graph_objs.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                                        yaxis=dict(range=[min(Y), max(Y)]))}

def find_dup(lst):
    dupItems = []
    if len(lst) != 0:
        uniqItems = {}
        for x in lst:
            if x not in uniqItems:
                uniqItems[x] = 1
            else:
                if uniqItems[x] == 1:
                    dupItems.append(x)
                uniqItems[x] += 1
        print(f'duplicate!: {len(dupItems)}')

if __name__ == "__main__":
    app.run_server(debug=True)
