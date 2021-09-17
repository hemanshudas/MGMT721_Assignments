import os
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from plotly.subplots import make_subplots



def calc_cost_ratio(w, r, s):
    u = r - w  # underage
    o = w - s  # overage

    return u/(u+o)

def calc_optim_q(var, mu, sigma):
    optim_q = norm.ppf(var, mu, sigma)

    return optim_q


''' Different items '''
r = 2                                   #revenue
w = 1                                   #wholesale_color
s = [0.75, 0.8, 0.7, 0.75]
color_mu = [800, 300, 600, 400]         #mean_demand
color_sigma = [300, 170, 200, 130]      #stddev_supply

optimal_q = []

for i in range(4):
    val = calc_optim_q(calc_cost_ratio(w, r, s[i]), color_mu[i], color_sigma[i])
    optimal_q.append(np.round(val,0))


''' Greige Tshirts '''
s = 0.8
r = 2
w = 1.1
greige_mu = 2100
greige_sigma = 419.285

greige_optim_q = calc_optim_q(calc_cost_ratio(w, r, s), greige_mu, greige_sigma)

def calc_loss_demanduncertainty(sigma, w, r, s):

    var = calc_cost_ratio(w, r, s)
    val = sigma * (r-s) * norm.pdf(norm.ppf(var))
    #print(np.round(norm.pdf(norm.ppf(var)),0))
    return val

def expected_profit(r, w, s, mu, sigma):
    profit_val = (r-w)*mu - calc_loss_demanduncertainty(sigma, w, r, s)
    return profit_val


greige_expected_profit = expected_profit(2, 1.1, 0.8, 2100, 419.28)

#greige_expected_profit = (r-w)*greige_mu - calc_loss_demanduncertainty(calc_cost_ratio(w,r,s), greige_sigma, r, s)