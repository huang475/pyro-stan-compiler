from pdb import set_trace as bb 
import pystan
import json
import os

def run_stan_advi(model_fname, data_fname, iters=1000):
    data = load_data(data_fname)
    print("loaded data with %d params = %s" % (len(data), data.keys()))
    with open(model_fname,"r") as f:
        code = f.read()
        
    sm = pystan.StanModel(model_code=code)
    fit = sm.vb(data=data, iter=iters)
    # print(fit)
    #  fit.keys()
    # ['args', 'inits', 'sampler_params', 'sampler_param_names', 'mean_pars']
    # fit['args'] has arguments for the ADVI algorithm
    # fit['sampler_params'] has as many samples for each param as #iters
    # fit['inits'] ??
    # fit['sampler_param_names'] has all names of parameters
    # fit['mean_pars'] has all learned means
    
    bb()
    
    
def load_data(fname):
    with open(fname,"r") as f:
        rdata = json.load(f)
    assert len(rdata) == 2
    data = {}
    n = len(rdata[0])
    for i in range(n):
        key = rdata[0][i]
        data[key] = rdata[1][i]
    return data

if not os.path.exists("model.data.json"):
    os.system("Rscript transform.R")
    
run_stan_advi("model.stan", "model.data.json")