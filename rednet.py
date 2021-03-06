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
    """construct network from comment object

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
    G.add_node(
        node.id,name=get_author(node),body=node.body,
        time=node.created_utc,count=d[node.author.name],
        score=node.score
        )
    for item in comment_list:
        local_id = item.id
        nodes.append(item)
        G.add_node(
            item.id,name=get_author(item),body=item.body,
            time=item.created_utc,count=d[get_author(item)],
            score=item.score
            )
        if item.parent_id[:2] != 't3':
            parent_id = item.parent_id.rsplit('t1_')[1]
            G.add_edge(parent_id, local_id)
    return G


def get_net(url):
    """construct comment network from url and get relevant info for plotting it

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
        submission title

    """
    reddit_api = np.load('./reddit_api.npz')
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
                     line=dict(width=3, color='rgb(250,250,250)'),
                     opacity=1,
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
        opacity=.7,
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=30,
            # colorbar=dict(
            #     thickness=35,
            #     title='Node Connections',
            #     xanchor='left',
            #     titleside='right'
            # ),
            line=dict(width=2)))

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([reddit.comment(adjacencies[0]).score])
        node_info =  wrap_wrapper(
            reddit.comment(adjacencies[0]).body
            )
        node_trace['text']+=tuple([node_info])

    return node_trace, edge_trace, submission.title
