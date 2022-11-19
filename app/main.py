import numpy as np
import networkx as nx
from bokeh.palettes import Category20_20
from bokeh.models import Circle, MultiLine, EdgesAndLinkedNodes, HoverTool, ColumnDataSource
from bokeh.models.widgets.markups import Div
from bokeh.plotting import figure, from_networkx, show,curdoc
from bokeh.transform import linear_cmap
from bokeh.models import CustomJS, Slider
from bokeh.layouts import column,row
import pathlib
import grapher
import histo

import matplotlib.pyplot as plt
path = pathlib.Path(__file__).parent.resolve()

original_matrix = np.load(str(path)+"/../data/plm_model.npy")
original_matrix.astype(np.float32)
diagonal = original_matrix.diagonal()
np.fill_diagonal(original_matrix, 0)
threshold = 0.000
threshold_line_source = ColumnDataSource(data={'x':[threshold,threshold],'y':[0.001,10]})

matrix = np.copy(original_matrix)
# storing diagonal values, if ever needed
diagonal = matrix.diagonal()
np.fill_diagonal(matrix, 0)
# === title
title = Div( text ="<h1> PLM Brain Vis </h1>")
# === create first graph
graph, ntw = grapher.create_graph(matrix, mscale=original_matrix.std()*3)
ntw.renderers.append(graph)
# === add slider
slider = Slider(start=-10, end=0, value=-10, step=1, title="ln threshold")
# === add Div for information
threshold_description = Div( text =" threshold: "+str(0), name="thr out")

# === add histogram
histplot = histo.create_histo(
    matrix.ravel(),
    bins= np.linspace(matrix.min(), matrix.max(),128),
    loglog=True, threshold=threshold_line_source)

def update(attr, old, new):
    """Interactively reconstruct the network as the threshold changes"""
    matrix = np.copy(original_matrix)

    threshold = np.exp(new)
    matrix[(original_matrix>-threshold)*(original_matrix<threshold)] = 0

    newgraph, newntw = grapher.create_graph(matrix,mscale=original_matrix.std()*3)
    newntw.renderers.append(newgraph)


    # update the objects on the page
    layout.children[1].children[0] = newntw
    threshold_description.text = f"threshold: {threshold}"
    threshold_line_source.data = {'x':[threshold,threshold],'y':[0.001,10]}




slider.on_change('value', update)

# Add some new columns to the node renderer data source
# graph.node_renderer.data_source.data['index'] = list(range(len(G)))
# graph.node_renderer.data_source.data['colors'] = Category20_20

# graph.node_renderer.glyph.update(size=20, fill_color="colors")
layout =column(title, row( ntw,column(slider,threshold_description,histplot)))
curdoc().add_root(layout)
curdoc().title = "PLM Brain Vis"
