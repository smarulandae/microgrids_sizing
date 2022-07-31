# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:14:21 2022

@author: pmayaduque
"""

from utilities import read_data, create_objects, create_technologies, calculate_energy, interest_rate
from utilities import fiscal_incentive 
import opt as opt
import pandas as pd 
from plotly.offline import plot
pd.options.display.max_columns = None
import time

# file paths github
demand_filepath = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/demand_SA.csv' 
forecast_filepath = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/forecast_SA.csv' 
units_filepath  = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/parameters_SA.json' 
# file paths local San Andrés
demand_filepath = "../data/San_Andres/demand_SA.csv"
forecast_filepath = '../data/San_Andres/forecast_SA.csv'
units_filepath = "../data/San_Andres/parameters_SA.json"
instanceData_filepath = "../data/San_Andres/instance_data_SA.json"
# file paths local Leticia
demand_filepath = "../data/Leticia/demand_L.csv"
forecast_filepath = '../data/Leticia/forecast_L.csv'
units_filepath = "../data/Leticia/parameters_L.json"
instanceData_filepath = "../data/Leticia/instance_data_L.json"
# file paths local Providencia
demand_filepath = "../data/Providencia/demand_P.csv"
forecast_filepath = '../data/Providencia/forecast_P.csv'
units_filepath = "../data/Providencia/parameters_P.json"
instanceData_filepath = "../data/Providencia/instance_data_P.json"
# file paths local Puerto Nariño
demand_filepath = "../data/Puerto_Nar/demand_PN.csv"
forecast_filepath = '../data/Puerto_Nar/forecast_PN.csv'
units_filepath = "../data/Puerto_Nar/parameters_PN.json"
instanceData_filepath = "../data/Puerto_Nar/instance_data_PN.json"
# file paths local TEST
demand_filepath = "../data/Test/demand_day.csv"
forecast_filepath = '../data/Test/forecast_day.csv'
units_filepath = "../data/Test/parameters_Test.json"
instanceData_filepath = "../data/Test/instance_data_Test.json"
#fiscal Data
fiscalData_filepath = "../data/fiscal_incentive.json"


time_i_create_data = time.time() #initial time
time_i_total = time.time()

# read data
demand_df, forecast_df, generators, batteries, instance_data, fisc_data = read_data(demand_filepath,
                                                                                    forecast_filepath,
                                                                                    units_filepath,
                                                                                    instanceData_filepath,
                                                                                    fiscalData_filepath)


# Create objects and generation rule
generators_dict, batteries_dict = create_objects(generators,
                                                 batteries, 
                                                 forecast_df,
                                                 demand_df,
                                                 instance_data)

#Create technologies and renewables set
technologies_dict, renewables_dict = create_technologies (generators_dict,
                                                          batteries_dict)



#Demand to be covered
demand_df['demand'] = instance_data['demand_covered']  * demand_df['demand'] 

#Calculate interest rate
ir = interest_rate(instance_data['i_f'],instance_data['inf'])

#Set GAP
MIP_GAP = 0.01
TEE_SOLVER = True
OPT_SOLVER = 'gurobi'

#Calculate fiscal incentives
delta = fiscal_incentive(fisc_data['credit'], 
                         fisc_data['depreciation'],
                         fisc_data['corporate_tax'],
                         ir,
                         fisc_data['T1'],
                         fisc_data['T2'])

time_f_create_data = time.time() - time_i_create_data #final time create

time_i_make_model = time.time()
# Create model          
model = opt.make_model(generators_dict, 
                       batteries_dict, 
                       dict(zip(demand_df.t, demand_df.demand)),
                       technologies_dict, 
                       renewables_dict, 
                       amax = instance_data['amax'], 
                       fuel_cost =  instance_data['fuel_cost'],
                       ir = ir, 
                       nse = instance_data['nse'], 
                       maxtec = instance_data['maxtec'], 
                       mintec = instance_data['mintec'], 
                       maxbr = instance_data['max_brand'],
                       years = instance_data['years'],
                       w_cost = instance_data['w_cost'],
                       tlpsp = instance_data['tlpsp'],
                       delta = delta)    


print("Model generated")

time_f_make_model = time.time() - time_i_make_model #final time create
# solve model 

time_i_solve = time.time()
results, termination = opt.solve_model(model, 
                                        optimizer = OPT_SOLVER,
                                        mipgap = MIP_GAP,
                                         tee = TEE_SOLVER)
print("Model optimized")
time_f_solve = time.time() - time_i_solve

time_i_results = time.time()
if termination['Temination Condition'] == 'optimal': 
   model_results = opt.Results(model)
   print(model_results.descriptive)
   print(model_results.df_results)
   generation_graph = model_results.generation_graph()
   plot(generation_graph)
   try:
       percent_df, energy_df, renew_df, total_df, brand_df = calculate_energy(batteries_dict, generators_dict, model_results, demand_df)
   except KeyError:
       pass

time_f_results = time.time() - time_i_results
time_f_total = time.time() - time_i_total

dict_times = {}
dict_times['Total'] = time_f_total
dict_times['Create Data'] = time_f_create_data
dict_times['Make model'] = time_f_make_model
dict_times['Solve'] = time_f_solve
dict_times['Results'] = time_f_results

df_times = pd.DataFrame(dict_times.items(), columns = ['Time Measure', 'Time Value'])

def multiple_dfs(df_list, sheets, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    col = 0
    for dataframe in df_list:
        dataframe.to_excel(writer,sheet_name=sheets,startrow=0 , startcol=col)   
        col = col + 4
    writer.save()

# list of dataframes
dfs = [df_times]

# run function
multiple_dfs(dfs, 'ExecTime', 'test_results.xlsx') 
'''
TRM = 3910
LCOE_COP = TRM * model_results.descriptive['LCOE']
model_results.df_results.to_excel("results.xlsx") 
'''