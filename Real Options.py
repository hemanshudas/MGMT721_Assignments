import os
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from plotly.subplots import make_subplots

r = 100
w = 50
s = 20
m = 30
ro_mu = 1000
ro_sigma = 300

'''Option A'''
c_a = 40 #Option Cost
x_a = 9 #Manufacturer Price

'''Option B'''
c_b = 6.5 #Option Cost
x_b = 48 #Manufacturer Price

'''Opportunity costs'''
def calc_opp_ratio(r, x, c):
    k_u = r - x - c
    k_o = c
    
    return k_u/(k_u + k_o)

def calc_optim_q(mu, sigma, r, x, c):
    var = calc_opp_ratio(r, x, c)
    optim_q = norm.ppf(var, mu, sigma)

    return optim_q

def calc_loss_demanduncertainty(sigma, r, x, c):
    var = calc_opp_ratio(r, x, c)
    val = sigma * (r - x) * norm.pdf(norm.ppf(var))
    # print(np.round(norm.pdf(norm.ppf(var)),0))
    return val

def retailer_exp_profit(mu,sigma, r, x, c):
    g_q = calc_loss_demanduncertainty(sigma, r, x, c)
    exp_profit = (r-x-c)*mu - g_q
    
    return exp_profit

def manf_exp_profit(mu, sigma, r, m, s, x, c):
    var = calc_opp_ratio(r, x, c)
    demand_margin = (c+x-m)*mu
    manf_g_q = sigma * (x-s)* norm.pdf(norm.ppf(var))
    manf_s_q = sigma * (m - s - (c*(r-s)/(r-x))) * norm.ppf(var)

    return demand_margin - manf_g_q - manf_s_q

def calc_cost_ratio(r, w, s):
    u = r - w  # underage
    o = w - s  # overage

    return u/(u+o)

def calc_optim_q_integrated(mu, sigma, r, w, s):
    var = calc_cost_ratio(r, w, s)
    optim_q = norm.ppf(var, mu, sigma)

    return optim_q

def calc_exp_profit(mu,  sigma, r, w, s):
    var = calc_cost_ratio(r, w, s)
    val = sigma * (r-s) * norm.pdf(norm.ppf(var))
    exp_pi = ((r-w)*mu) - val
    return exp_pi

#Real Options
retailA_pi = retailer_exp_profit(ro_mu, ro_sigma, r, x_a, c_a)
qA = calc_optim_q(ro_mu, ro_sigma, r, x_a, c_a)
manfA_pi = manf_exp_profit(ro_mu, ro_sigma, r, m, s, x_a, c_a)
print('Option A')
print(qA)
print(retailA_pi)
print(manfA_pi)
print(retailA_pi + manfA_pi)

retailB_pi = retailer_exp_profit(ro_mu, ro_sigma, r, x_b, c_b)
qB = calc_optim_q(ro_mu, ro_sigma, r, x_b, c_b)
manfB_pi = manf_exp_profit(ro_mu, ro_sigma, r, m, s, x_b, c_b)
print('Option B')
print(qB)
print(retailB_pi)
print(manfB_pi)
print(retailB_pi + manfB_pi)


print('Merged')
#Vertical Integration
optim_q = calc_optim_q_integrated(ro_mu, ro_sigma, r, m, s)
exp_profit = calc_exp_profit(ro_mu, ro_sigma, r, m, s)
print(optim_q)
print(exp_profit)
'''
def calc_rel(r, m, s, x):
    val = (r-x) - ((r-m)*(r-x)/(r-s))
    return val

fig = go.Figure()
x_d = np.linspace(0, r, 100)
fig.add_trace(go.Scatter(x= x_d, y= calc_rel(r,m, s, x_d)))
fig.show()
'''