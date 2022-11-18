import numpy as np
import networkx as nx
from bokeh.palettes import Category20_20
from bokeh.models import Circle, MultiLine, EdgesAndLinkedNodes, HoverTool
from bokeh.plotting import figure, from_networkx, show,curdoc
from bokeh.transform import linear_cmap
from bokeh.models import CustomJS, Slider
from bokeh.layouts import column,row
import pathlib

import matplotlib.pyplot as plt
path = pathlib.Path(__file__).parent.resolve()

original_matrix = np.load(str(path)+"/../data/plm_model.npy")
diagonal = original_matrix.diagonal()
np.fill_diagonal(original_matrix, 0)
a = 0.000
matrix = np.copy(original_matrix)
# matrix[(original_matrix>-a)*(original_matrix<a)]=0
max_j = matrix.max()

diagonal = matrix.diagonal()
np.fill_diagonal(matrix, 0)
G = nx.from_numpy_matrix(matrix)


for u,v,a in G.edges(data=True):
    a['scaled_abs_weight']=abs(a['weight'])/max_j*5
    a['sign']=np.sign(a['weight'])

# print(G.edges(data=True))

p = figure(x_range=(-2, 2), y_range=(-2, 2),
           x_axis_location=None, y_axis_location=None,
           tools="",)
p.grid.grid_line_color = None

graph = from_networkx(G, nx.spring_layout, scale=1.8, center=(0,0))
graph.node_renderer.glyph = Circle(
    size=10,
    fill_color=linear_cmap('index', 'Spectral8', min(G.nodes()), max(G.nodes()))
)
graph.edge_renderer.glyph = MultiLine(line_color=linear_cmap('sign', 'RdBu8', matrix.min(),matrix.max()),
    line_alpha='scaled_abs_weight',
    line_width="scaled_abs_weight"
    )
graph.inspection_policy=EdgesAndLinkedNodes()
p.renderers.append(graph)


def update(attr, old, new):
    newplot = figure(x_range=(-2, 2), y_range=(-2, 2),
               x_axis_location=None, y_axis_location=None,
               tools="",)
    threshold = np.exp(new)
    print(threshold)
    matrix = np.copy(original_matrix)
    matrix[(original_matrix>-threshold)*(original_matrix<threshold)] = 0
    newG = nx.from_numpy_matrix(matrix)
    for u,v,a in newG.edges(data=True):
        a['scaled_abs_weight']=abs(a['weight'])/max_j*5
        a['sign']=np.sign(a['weight'])
    newgraph = from_networkx(newG, nx.spring_layout, scale=1.8, center=(0,0))
    # newplot.add_tools(hover)
    # p.grid.grid_line_color = None
    newgraph.node_renderer.glyph = Circle(
        size=10,
        fill_color=linear_cmap('index', 'Spectral8', min(G.nodes()), max(G.nodes()))
    )
    newgraph.edge_renderer.glyph = MultiLine(line_color=linear_cmap('sign', 'RdBu8', matrix.min(),matrix.max()),
        line_alpha='scaled_abs_weight',
        line_width="scaled_abs_weight"
        )

    newgraph.inspection_policy=EdgesAndLinkedNodes()
    newplot.renderers.append(newgraph)
    newplot.add_tools(HoverTool(
    tooltips=[
        ( 'weight', '@weight'      ),
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    # mode='vline'
))

    # update the layout
    layout.children[0] = newplot

slider = Slider(start=-10, end=0, value=-10, step=1, title="ln threshold")
slider.on_change('value', update)
# Add some new columns to the node renderer data source
# graph.node_renderer.data_source.data['index'] = list(range(len(G)))
# graph.node_renderer.data_source.data['colors'] = Category20_20

# graph.node_renderer.glyph.update(size=20, fill_color="colors")
layout = row( p,slider)
curdoc().add_root(layout)
