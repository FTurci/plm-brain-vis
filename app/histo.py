import numpy as np
from bokeh.layouts import column,row
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show


def create_histo(data, bins,fill_color='navy', line_color='grey',alpha=0.5, log=False, loglog=False):
    """Create histogram from data."""


    hist, edges = np.histogram(data, bins=bins, density=True)
    y = hist
    x= edges
    if loglog:
        logy= np.log10(hist)

        # plot positive branch
        p1 = figure( tools='', background_fill_color="#fafafa",x_axis_type="log",y_axis_type="log")
        valid =x>0
        logx = np.log10(x[valid])
        p1.line(x[valid], y[valid[:-1]],line_color='red')
        p1.circle(x[valid], y[valid[:-1]],fill_color='red',line_color='red')
        p1.title='positive couplings'

        p2 = figure( tools='', background_fill_color="#fafafa",x_axis_type="log",y_axis_type="log")
        valid =x<0
        mx = -x
        p2.line(mx[valid], y[valid[:-1]], line_color='navy')
        p2.circle(mx[valid], y[valid[:-1]], fill_color='navy',line_color='navy')
        p2.title='negative couplings'
        # p2.quad(top=y[valid[:-1]], bottom=0, left=logx[:-1], right=logx[1:],
               # fill_color='red', line_color=line_color, alpha=alpha)

        for p in p1,p2:
            # p.y_range.start = 0
            p.xgrid.visible = False
            p.ygrid.visible = False
            p.plot_height=200
            p.plot_width=400
            p.toolbar.logo = None

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
