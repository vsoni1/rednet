"""
functions for generating network plot data from reddit conversation
"""
import plotly.graph_objs as go
import networkx as nx
import praw
import numpy as np
from collections import Counter
import textwrap

def wrap_wrapper(text):
    """returns wrapped text, so it doesn't get cut off during hover over
    """
    textlist = textwrap.wrap(text,width=30)
    wrappedtext = ''
    for item in textlist:
        wrappedtext+=item
        wrappedtext+='<br>'
    return wrappedtext

def make_comment_net(node):
    """extract profile of bright region in image

    Parameters
    ----------
    node : PRAW Comment object

    Returns
    -------
    Graph
        networkx graph object with nodes as comment ids and attributes include
        comment body, time, and number of replies

    """
    def get_author(n):
        try:
            return n.author.name
        except:
            return 'N/A'
    G = nx.Graph()
    nodes = []
    comment_list = node.replies.list()
    nodelist = np.append(node,comment_list)
    authors = [get_author(n) for n in nodelist]
    d = Counter(authors)
    G.add_node(node.id,name=get_author(node),body=node.body,time=node.created_utc,count=d[node.author.name])
    for item in comment_list:
        local_id = item.id
        nodes.append(item)
        G.add_node(item.id,name=get_author(item),body=item.body,time=item.created_utc,count=d[get_author(item)])
        if item.parent_id[:2] != 't3':
            parent_id = item.parent_id.rsplit('t1_')[1]
            G.add_edge(parent_id, local_id)
    return G


def get_net(url):
    """extract profile of bright region in image

    Parameters
    ----------
    url : url of reddit submission

    Returns
    -------
    node_trace
        nodes of network plot
    edge_trace
        edges of network plot
    title
        submissino title

    """
    reddit_api = np.load('/home/vsoni1/reddit_api.npz')
    reddit = praw.Reddit(client_id=reddit_api['client_id'],
                          client_secret=reddit_api['client_secret'],
                          user_agent=reddit_api['user_agent'])

    id = np.array(url.rsplit('/'))[np.argwhere(
        np.array(url.rsplit('/'))=='comments'
        )[0]+1][0]

    submission = reddit.submission(id=id)#sort[0] #taken from psaw grabbed data
    submission.comments.replace_more(limit=None, threshold=0)
    all_comments = submission.comments
    node = all_comments[0]

    G = make_comment_net(node)
    pos = nx.spring_layout(G, k=.5, iterations=500)

    Xe=[]
    Ye=[]
    for e in G.edges():
        Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
        Ye.extend([pos[e[0]][1], pos[e[1]][1], None])

    edge_trace=dict(type='scatter',
                     mode='lines',
                     x=Xe,
                     y=Ye,
                     line=dict(width=1, color='rgb(25,25,25)'),
                     hoverinfo='none'
                    )

    Xn=[pos[p][0] for p in pos]
    Yn=[pos[p][1] for p in pos]

    node_trace = go.Scatter(
        x=Xn,
        y=Yn,
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info =  wrap_wrapper(
            reddit.comment(adjacencies[0]).body
            )
        node_trace['text']+=tuple([node_info])

    return node_trace, edge_trace, submission.title
