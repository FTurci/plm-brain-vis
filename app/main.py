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

# load coupling matrix 
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
# load node information
node_info = np.genfromtxt(str(path)+"/../data/roi_clusters.csv",delimiter=",", skip_header=1,dtype=str)

cluster_type = {i:node_info[:,-1][i] for i  in range(node_info.shape[0])}
# print(cluster_type)
# === title
title = Div( text ="<h1> PLM Brain Vis </h1>")
# === create first graph
G, graph, ntw = grapher.create_graph(matrix, mscale=original_matrix.std()*3,type=cluster_type)
# print(nx.get_node_attributes(G,"type"))
degrees_source = ColumnDataSource(data={'degrees':np.array([d[1] for d in G.degree()])})
count_deg_source = ColumnDataSource(histo.hist_deg(degrees_source))
ntw.renderers.append(graph)
# === add slider
slider = Slider(start=-10, end=0, value=-10, step=1, title="ln threshold")
# === add Div for information
threshold_description = Div( text =" threshold: "+str(0), name="thr out")

# === add histograms of couplings
histplot = histo.create_threshold_hists(
    matrix.ravel(),
    bins= np.linspace(matrix.min(), matrix.max(),128),
    loglog=True, threshold=threshold_line_source)
# add degree distribution
degdist = histo.create_degree_hist(count_deg_source)

def update(attr, old, new):
    """Interactively reconstruct the network as the threshold changes"""
    matrix = np.copy(original_matrix)

    threshold = np.exp(new)
    matrix[(original_matrix>-threshold)*(original_matrix<threshold)] = 0

    newG, newgraph, newntw = grapher.create_graph(matrix,mscale=original_matrix.std()*3,type=cluster_type)
    newntw.renderers.append(newgraph)

    # update the objects on the page
    layout.children[1].children[0] = newntw
    threshold_description.text = f"threshold: {threshold}"
    threshold_line_source.data = {'x':[threshold,threshold],'y':[0.001,10]}
    degrees_source.data =  {'degrees':np.array([d[1] for d in newG.degree()]) }
    count_deg_source.data = histo.hist_deg(degrees_source)




slider.on_change('value', update)

# Add some new columns to the node renderer data source
# graph.node_renderer.data_source.data['index'] = list(range(len(G)))
# graph.node_renderer.data_source.data['colors'] = Category20_20

# graph.node_renderer.glyph.update(size=20, fill_color="colors")
layout =column(title, row( ntw,column(
    slider,
    threshold_description,
    histplot,
    degdist,
    Div( text =''',a href="https://github.com/maxkloucek"> Maximilian Kloucek</a> & <a href="https://francescoturci.net"> Francesco Turci </a>''')
)))
curdoc().add_root(layout)
curdoc().title = "PLM Brain Vis"
