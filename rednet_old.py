# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import networkx as nx
# import praw
# import numpy as np
# from collections import Counter
# import textwrap

# # import plotly.plotly as py

# reddit = praw.Reddit(client_id='fAT8FETUwusAZg',
#                       client_secret='JWdrt4geIOwH1pmSeiOqWxhSlzA',
#                       user_agent='test')

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# def wrap_wrapper(text):
#     textlist = textwrap.wrap(text,width=30)
#     wrappedtext = ''
#     for item in textlist:
#         wrappedtext+=item
#         wrappedtext+='<br>'
#     return wrappedtext

# def make_comment_net(node):
#     #get_author avoids error from the fact that deleted comments have None as author
#     def get_author(n):
#         try:
#             return n.author.name
#         except:
#             return 'N/A'
#     G = nx.Graph()
#     nodes = []
#     edges = []

#     comment_list = node.replies.list()

#     nodelist = np.append(node,comment_list)
#     authors = [get_author(n) for n in nodelist]
#     d = Counter(authors)
#     n, m = d.keys(), d.values()

#     G.add_node(node.id,name=get_author(node),body=node.body,time=node.created_utc,count=d[node.author.name])
#     for item in comment_list:
#         local_id = item.id
#         nodes.append(item)
#         G.add_node(item.id,name=get_author(item),body=item.body,time=item.created_utc,count=d[get_author(item)])
#         if item.parent_id[:2] != 't3':
#             parent_id = item.parent_id.rsplit('t1_')[1]
#             G.add_edge(parent_id, local_id)
#     return G

# url = 'https://www.reddit.com/r/Kanye/comments/a6qizz/yandhi_gone_be_a_610_bois/'
# id=np.array(url.rsplit('/'))[np.argwhere(
#     np.array(url.rsplit('/'))=='comments'
# )[0]+1][0]

# submission = reddit.submission(id=id)#sort[0] #taken from psaw grabbed data
# submission.comments.replace_more(limit=None, threshold=0)
# all_comments = submission.comments
# node = all_comments[0]

# G = make_comment_net(node)
# # G=nx.random_geometric_graph(200,0.125)
# pos = nx.spring_layout(G, k=.5, iterations=500)

# Xe=[]
# Ye=[]
# for e in G.edges():
#     Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
#     Ye.extend([pos[e[0]][1], pos[e[1]][1], None])

# edge_trace=dict(type='scatter',
#                  mode='lines',
#                  x=Xe,
#                  y=Ye,
#                  line=dict(width=1, color='rgb(25,25,25)'),
#                  hoverinfo='none'
#                 )

# Xn=[pos[p][0] for p in pos]
# Yn=[pos[p][1] for p in pos]

# node_trace = go.Scatter(
#     x=Xn,
#     y=Yn,
#     text=[],
#     mode='markers',
#     hoverinfo='text',
#     marker=dict(
#         showscale=True,
#         # colorscale options
#         #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
#         #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
#         #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
#         colorscale='YlGnBu',
#         reversescale=True,
#         color=[],
#         size=10,
#         colorbar=dict(
#             thickness=15,
#             title='Node Connections',
#             xanchor='left',
#             titleside='right'
#         ),
#         line=dict(width=2)))

# for node, adjacencies in enumerate(G.adjacency()):
#     node_trace['marker']['color']+=tuple([len(adjacencies[1])])
#     node_info =  wrap_wrapper(
#         reddit.comment(adjacencies[0]).body
#         )
#     node_trace['text']+=tuple([node_info])

# axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
#           zeroline=False,
#           showgrid=False,
#           showticklabels=False,
#           title=''
#           )
# layout=dict(title= submission.title,
#             font= dict(family='Balto'),
#             width=700,
#             height=700,
#             autosize=False,
#             showlegend=False,
#             xaxis=axis,
#             yaxis=axis,
#             margin=dict(
#             l=40,
#             r=40,
#             b=85,
#             t=100,
#             pad=0,

#     ),
#     hovermode='closest',
#     plot_bgcolor='#efecea', #set background color
#     )
# app.layout = html.Div([
#     dcc.Graph(
#         id='network',
#         figure={
#             'data': [
#                 node_trace,edge_trace
#             ],
#             'layout': layout
#         }
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)