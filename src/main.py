# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:14:21 2022

@author: pmayaduque
"""

from utilities import read_data, create_objects, create_technologies, calculate_energy
import opt as opt
import pandas as pd 
from plotly.offline import plot
pd.options.display.max_columns = None

# file paths github
demand_filepath = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/demand_SA.csv' 
forecast_filepath = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/forecast_SA.csv' 
units_filepath  = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/parameters_SA.json' 
# file paths local SA
demand_filepath = "../data/San_Andres/demand_SA.csv"
forecast_filepath = '../data/San_Andres/forecast_SA.csv'
units_filepath = "../data/San_Andres/parameters_SA.json"
instanceData_filepath = "../data/San_Andres/instance_data_SA.json"
# file paths local PR
demand_filepath = "../data/Providencia/demand_P.csv"
forecast_filepath = '../data/Providencia/forecast_P.csv'
units_filepath = "../data/Providencia/parameters_P.json"
instanceData_filepath = "../data/Providencia/instance_data_P.json"
# file paths local PN
demand_filepath = "../data/Puerto_Nar/demand_PN.csv"
forecast_filepath = '../data/Puerto_Nar/forecast_PN.csv'
units_filepath = "../data/Puerto_Nar/parameters_PN.json"
instanceData_filepath = "../data/Puerto_Nar/instance_data_PN.json"
# file paths local TEST
demand_filepath = "../data/Test/demand_day.csv"
forecast_filepath = '../data/Test/forecast_day.csv'
units_filepath = "../data/Test/parameters_Test.json"
instanceData_filepath = "../data/Test/instance_data_Test.json"

# read data
demand_df, forecast_df, generators, batteries, instance_data = read_data(demand_filepath,
                                                          forecast_filepath,
                                                          units_filepath,
                                                          instanceData_filepath)




# Create objects and generation rule
generators_dict, batteries_dict = create_objects(generators,
                                                 batteries, 
                                                 forecast_df,
                                                 demand_df,
                                                 instance_data)

#Create technologies and renewables set
technologies_dict, renewables_dict = create_technologies (generators_dict,
                                                          batteries_dict)



# Create model          
model = opt.make_model(generators_dict, 
                       batteries_dict, 
                       dict(zip(demand_df.t, demand_df.demand)),
                       technologies_dict, 
                       renewables_dict, 
                       amax = instance_data['amax'], 
                       fuel_cost =  instance_data['fuel_cost'],
                       ir = instance_data['ir'], 
                       nse = instance_data['nse'], 
                       maxtec = instance_data['maxtec'], 
                       mintec = instance_data['mintec'], 
                       maxbr = instance_data['max_brand'],
                       years = instance_data['years'],
                       w_cost = instance_data['w_cost'],
                       tlpsp = instance_data['tlpsp'])    


print("Model generated")
# solve model 
results, termination = opt.solve_model(model, 
                       optimizer = 'gurobi',
                       mipgap = 0.01,
                       tee = True)
print("Model optimized")


#TODO:  ext_time?
if termination['Temination Condition'] == 'optimal': 
   model_results = opt.Results(model)
   print(model_results.descriptive)
   print(model_results.df_results)
   generation_graph = model_results.generation_graph()
   plot(generation_graph)
   percent_df, energy_df, renew_df, total_df, brand_df = calculate_energy(batteries_dict, generators_dict, model_results, demand_df)
