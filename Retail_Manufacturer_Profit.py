import os
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from plotly.subplots import make_subplots

def fig_update_layout(fig, update_height, update_width, legend_text):
    fig.update_layout(#legend_title_text=legend_text,
                      legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=1
        ), height=update_height, width=update_width, showlegend=True)

    fig.update_layout(margin_r=10, margin_l=10, margin_t=20, margin_b=20)

    return fig

s = 20 #salvage cost
m = 30 #production cost
r = 100 #revenue per item

d_mu = 1000
d_sigma = 300

def calc_cost_ratio(w):
    u = r - w  # underage
    o = w - s  # overage

    return u/(u+o)

def calc_cost_ratio_manf(w):
    u = w - m  # underage
    o = m  # overage

    return u/(u+o)


def calc_optim_q(var):
    optim_q = norm.ppf(var, d_mu, d_sigma)

    return optim_q

def calc_loss_demanduncertainty(var, sigma, r, s):
    val = sigma * (r-s) * norm.pdf(norm.ppf(var))

    return val

''' Q1 Wholesale Price '''

val_w = np.linspace(31, 99, (99-30))

profit_manufacturer = (val_w - m)*calc_optim_q(calc_cost_ratio(val_w))
profit_retailer = (r-val_w)*d_mu - calc_loss_demanduncertainty(calc_cost_ratio(val_w), d_sigma, r, s)

#fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x = val_w, y = profit_retailer, mode = 'lines', name = '$\u03A0_{r}$'), secondary_y= False)
fig.add_trace(go.Scatter(x = val_w, y = profit_manufacturer, mode = 'lines', name = '$\u03A0_{m}$'), secondary_y= False)
fig.add_trace(go.Scatter(x = val_w, y = profit_manufacturer+profit_retailer, mode = 'lines', name = '$\u03A0_{m} + \u03A0_{r}$'), secondary_y= False)
fig.add_trace(go.Scatter(x = val_w, y = calc_optim_q(calc_cost_ratio(val_w)), mode = 'markers', name = '$q^{*}$'),secondary_y= True)
fig.add_trace(go.Scatter(x = val_w, y = calc_optim_q(calc_cost_ratio_manf(val_w)), mode = 'markers', name = '$q_{m}^{*}$'),secondary_y= True)

fig = fig_update_layout(fig, 600, 1200, 'Legend: ')
fig.update_yaxes(title_text="Expected Profit", secondary_y=False)
fig.update_yaxes(title_text="Optimal Order Quantity", secondary_y=True)
fig.update_xaxes(title_text="Wholesale Price (W)")
fig.show()
#fig.write_image('SDS721_WholesalePrice_16Sep_V2.jpg')


fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=val_w, y = (r-val_w)*d_mu, name = 'Sales Rev'))
fig2.add_trace(go.Scatter(x=val_w, y = calc_loss_demanduncertainty(calc_cost_ratio(val_w), d_sigma, r, s), name = 'Loss Function'))
fig2.add_trace(go.Scatter(x = val_w, y = profit_retailer, mode = 'lines', name = '$\u03A0_{r}$'))
fig2.show()

