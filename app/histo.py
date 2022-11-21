import numpy as np
from bokeh.layouts import column,row
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show
from bokeh.models import Band, ColumnDataSource

def hist_deg(degrees):
    bc = np.bincount(degrees.data['degrees'])
    ds = {'count':bc,'deg':np.arange(len(bc))}
    return ds


def create_degree_hist(datasource, fill_color='#008f51', line_color='#008f51',alpha=0.5, x_axis_type="linear",y_axis_type="linear"):

    p = figure( tools='', background_fill_color="#fafafa", x_axis_type=x_axis_type, y_axis_type=y_axis_type)
    p.line(x='deg', y='count',source=datasource,line_color=line_color)
    p.circle(x='deg', y='count',source=datasource,fill_color=fill_color, line_color=line_color)

    p.y_range.start = 0
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.plot_height=200
    p.plot_width=400
    p.toolbar.logo = None
    p.title='degree count'
    p.xaxis.axis_label = "degree"
    p.yaxis.axis_label = "count"
    return p

def create_threshold_hists(data, bins,fill_color='navy', line_color='grey',alpha=0.5, log=False, loglog=False ,threshold=0):
    """Create histograms for thesholds from data."""
    hist, edges = np.histogram(data, bins=bins, density=True)
    y = hist
    x= edges
    if loglog:
        logy= np.log10(hist)

        # plot positive branch
        p1 = figure( tools='', background_fill_color="#fafafa",x_axis_type="log",y_axis_type="log", name='positive')
        # centers
        xc = x[:-1]+(x[1]-x[0])/2
        valid =xc>0
        p1.line(xc[valid], y[valid],line_color='red')
        p1.circle(xc[valid], y[valid],fill_color='red',line_color='red')
        p1.line(x='x',y='y',source=threshold, line_color="black", name='tline')
        p1.title='positive couplings'
        p1.xaxis.axis_label = r"\[J_{ij}\]"

        p2 = figure( tools='', background_fill_color="#fafafa",x_axis_type="log",y_axis_type="log")
        valid =xc<0
        mx = -xc
        p2.line(mx[valid], y[valid], line_color='navy')
        p2.circle(mx[valid], y[valid], fill_color='navy',line_color='navy')
        p2.line(x='x',y='y',source=threshold, line_color="black", name='tline')
        p2.title='negative couplings'
        p2.xaxis.axis_label = r"\[-J_{ij}\]"
        # p2.quad(top=y[valid[:-1]], bottom=0, left=logx[:-1], right=logx[1:],
               # fill_color='red', line_color=line_color, alpha=alpha)
        # add lines based on threshold


        for p in p1,p2:
            # p.y_range.start = 0
            p.xgrid.visible = False
            p.ygrid.visible = False
            p.plot_height=200
            p.plot_width=400
            p.toolbar.logo = None
            
            p.yaxis.axis_label = "pdf"

        return column(p1,p2)


    else:

        if log==True:
            y= np.log10(hist)
        p = figure( tools='', background_fill_color="#fafafa")
        p.quad(top=y, bottom=0, left=x[:-1], right=x[1:],
               fill_color=fill_color, line_color=line_color, alpha=alpha)

        p.y_range.start = 0
        p.xgrid.visible = False
        p.ygrid.visible = False
        p.plot_height=200
        p.plot_width=400
        p.toolbar.logo = None
        return p
