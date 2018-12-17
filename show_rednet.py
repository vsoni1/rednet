"""
code for generating visualization of reddit conversation.
gets input url from user, and generates network from rednet.
This code plots it
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from rednet import get_net

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

app.layout = html.Div([
    html.Div('Please give it a second to load after clicking \'Submit\' '),
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    html.Div([
        dcc.Graph(
            id='network',

            config={
                'displayModeBar': False
            }
        )
    ])
])

@app.callback(
    dash.dependencies.Output('network', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    node_trace, edge_trace, title = get_net(str(value))
    layout=dict(title= title,
            font= dict(family='Balto'),
            width=1000,
            height=700,
            autosize=False,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,
            margin=dict(
            l=40,
            r=40,
            b=85,
            t=100,
            pad=0,

    ),
    hovermode='closest',
    plot_bgcolor='#efecea', #set background color
    )
    return {
                'data': [
                    node_trace, edge_trace
                ],
                'layout': layout
            }

if __name__ == '__main__':
    app.run_server(debug=True)