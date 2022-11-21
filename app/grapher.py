import networkx as nx
from bokeh.plotting import figure, from_networkx
from bokeh.transform import linear_cmap
from bokeh.models import Circle, MultiLine, EdgesAndLinkedNodes, HoverTool,BoxZoomTool,ResetTool
import numpy as np

def create_graph(matrix, scale=1.8,circlesize=10, xrange=(-2,2), yrange=(-2,2),mscale =1.0):
    """Create Bokeh network from numpy matrix"""

    G = nx.from_numpy_matrix(matrix)
    # create additional rescaled attributes
    for u,v,a in G.edges(data=True):
        a['scaled_abs_weight']=abs(a['weight'])/mscale
        a['sign']=np.sign(a['weight'])

    p = figure(x_range=xrange, y_range=yrange,
               x_axis_location=None, y_axis_location=None,
               tools="",)
    p.toolbar.logo = None


    graph = from_networkx(G, nx.spring_layout, scale=scale, center=(0,0))

    graph.node_renderer.glyph = Circle(
        size=circlesize,
        fill_color=linear_cmap('index', ('#ff9300', '#8df900'), min(G.nodes()), max(G.nodes()))
    )
    graph.edge_renderer.glyph = MultiLine(
        line_color=linear_cmap('sign', 'RdBu8', matrix.min(),matrix.max()),
        line_alpha='scaled_abs_weight',
        line_width="scaled_abs_weight"
        )
    graph.inspection_policy=EdgesAndLinkedNodes()
    p.add_tools(HoverTool(
        tooltips=[
            ( 'weight', '@weight'      ),
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        # mode='vline'
    )
    )
    p.add_tools(BoxZoomTool(),ResetTool())
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.name = "main"
    return G,graph,p
