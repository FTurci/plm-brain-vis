import networkx as nx

from bokeh.io import show, output_file, output_notebook, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral4

G = nx.karate_club_graph()
print(G.nodes[1]['club'])
plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Graph Interaction Demonstration"

node_hover_tool = HoverTool(tooltips=[('index', '@index'),
                                 ('club', '@club')])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0,0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

# This code will be change to "output_file("interactive_graphs.html")"
output_file("interactive_graphs.html")
# output_notebook()
show(plot)