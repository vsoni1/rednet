"""
code for generating visualization of reddit conversation.
gets input url from user, and generates network from rednet.
This code plots it
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from rednet import get_net

url = 'https://www.reddit.com/r/AMA/comments/8bh564/i_finished_an_entire_chapstick_without_losing_it/'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_fig(value):
    print(str(value))
    node_trace, edge_trace, title = get_net(str(value))
    print(title)
    return{
            'data': [
                edge_trace, node_trace
            ],
            'layout': get_layout(title)
            }
def get_layout(title):
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          fixedrange=True,
          title=''
          )
    layout=dict(title= str(title),
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
            t=30,
            pad=0,
            ),
    hovermode='closest',
    plot_bgcolor='rgb(50,50,100)', #set background color
    )
    return layout

app.layout = html.Div([
    html.Div('Please give it a second to load after clicking \'Submit\' '),
    html.Div(dcc.Input(id='input-box', type='text', value=url)),
    html.Button('Submit', id='button'),
    html.H2('Hover over the dots'),
    html.Div([
        dcc.Graph(
            id='network',
            config={
                'displayModeBar': False,
            }
        )
    ])
])

@app.callback(
    dash.dependencies.Output('network', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    fig = get_fig(value)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)