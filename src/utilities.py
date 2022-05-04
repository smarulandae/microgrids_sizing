# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:51:07 2022

@author: pmayaduque
"""
from classes import Solar, Eolic, Diesel, Battery
import pandas as pd
import requests
import json 
import numpy as np
import math


def read_data(demand_filepath, 
              forecast_filepath,
              units_filepath,
              instance_data):
    
    forecast_df = pd.read_csv(forecast_filepath)
    demand_df = pd.read_csv(demand_filepath)
    try:
        generators_data =  requests.get(units_filepath)
        generators_data = json.loads(generators_data.text)
    except:
        f = open(units_filepath)
        generators_data = json.load(f)    
    generators = generators_data['generators']
    batteries = generators_data['batteries']
    
    try:
        instance_data =  requests.get(instance_data)
        instance_data = json.loads(instance_data.text)
    except:
        f = open(instance_data)
        instance_data = json.load(f) 
    
    return demand_df, forecast_df, generators, batteries, instance_data

def create_objects(generators, batteries, forecast_df, demand_df):
    # Create generators and batteries
    generators_dict = {}
    for k in generators:
      if k['tec'] == 'S':
        obj_aux = Solar(*k.values())
        obj_aux.Solargeneration(forecast_df['Rt'])
      elif k['tec'] == 'W':
        obj_aux = Eolic(*k.values())
        obj_aux.Windgeneration(forecast_df['Wt'])
      elif k['tec'] == 'D':
        obj_aux = Diesel(*k.values())   
        obj_aux.Dieselgeneration(demand_df['demand'])
      generators_dict[k['id_gen']] = obj_aux
      
    batteries_dict = {}
    for l in batteries:
        obj_aux = Battery(*l.values())
        batteries_dict[l['id_bat']] = obj_aux
        batteries_dict[l['id_bat']].calculatesoc()
        
    # Create technologies dictionarry
    technologies_dict = dict()
    for bat in batteries_dict.values(): 
      if not (bat.tec in technologies_dict.keys()):
        technologies_dict[bat.tec] = set()
        technologies_dict[bat.tec].add(bat.br)
      else:
        technologies_dict[bat.tec].add(bat.br)
    for gen in generators_dict.values(): 
      if not (gen.tec in technologies_dict.keys()):
        technologies_dict[gen.tec] = set()
        technologies_dict[gen.tec].add(gen.br)
      else:
        technologies_dict[gen.tec].add(gen.br)

    # Creates renewables dict
    renewables_dict = dict()
    for gen in generators_dict.values(): 
        if gen.tec == 'S' or gen.tec == 'W': #or gen.tec = 'H'
          if not (gen.tec in renewables_dict.keys()):
              renewables_dict[gen.tec] = set()
              renewables_dict[gen.tec].add(gen.br)
          else:
              renewables_dict[gen.tec].add(gen.br)
              
    return generators_dict, batteries_dict, technologies_dict, renewables_dict


 
def calculate_sizingcost(generators_dict, batteries_dict, ir, years):
            expr = 0
            for gen in generators_dict.values(): 
                expr += gen.cost_up*gen.n 
                expr += gen.cost_r*gen.n 
                expr += gen.cost_om*gen.n 
                expr -= gen.cost_s*gen.n 
                
            for bat in batteries_dict.values(): 
                expr += bat.cost_up
                expr += bat.cost_om
                expr += bat.cost_r
                expr -= bat.cost_s
                
                
                
            TNPC = expr
            CRF = (ir * (1 + ir)**(years))/((1 + ir)**(years)-1) 

            return TNPC, CRF

