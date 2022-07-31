# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:14:21 2022

@author: pmayaduque
"""

from utilities import read_data, create_objects, create_technologies, calculate_energy, interest_rate
from utilities import fiscal_incentive 
import numpy as np
import opttest as opt
import copy
import random
import pandas as pd 
from plotly.offline import plot
pd.options.display.max_columns = None
import time

# file paths github
demand_filepath_git = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/demand_SA.csv' 
forecast_filepath_git = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/forecast_SA.csv' 
units_filepath_git  = 'https://raw.githubusercontent.com/pmayaduque/MicrogridSizing/main/data/San_Andres/parameters_SA.json' 
# file paths local TEST
demand_filepath_test = "../data/Test/demand_day.csv"
forecast_filepath_test = '../data/Test/forecast_day.csv'
units_filepath_test = "../data/Test/parameters_Test.json"
instanceData_filepath_test = "../data/Test/instance_data_Test.json"
# file paths local Puerto Nariño
demand_filepath_pn = "../data/Puerto_Nar/demand_PN.csv"
forecast_filepath_pn = '../data/Puerto_Nar/forecast_PN.csv'
units_filepath_pn = "../data/Puerto_Nar/parameters_PN.json"
instanceData_filepath_pn = "../data/Puerto_Nar/instance_data_PN.json"
# file paths local Leticia
demand_filepath_l = "../data/Leticia/demand_L.csv"
forecast_filepath_l = '../data/Leticia/forecast_L.csv'
units_filepath_l = "../data/Leticia/parameters_L.json"
instanceData_filepath_l = "../data/Leticia/instance_data_L.json"
# file paths local San Andrés
demand_filepath_sa = "../data/San_Andres/demand_SA.csv"
forecast_filepath_sa = '../data/San_Andres/forecast_SA.csv'
units_filepath_sa = "../data/San_Andres/parameters_SA.json"
instanceData_filepath_sa = "../data/San_Andres/instance_data_SA.json"
# file paths local Providencia
demand_filepath_p = "../data/Providencia/demand_P.csv"
forecast_filepath_p = '../data/Providencia/forecast_P.csv'
units_filepath_p = "../data/Providencia/parameters_P.json"
instanceData_filepath_p = "../data/Providencia/instance_data_P.json"

#fiscal Data
fiscalData_filepath = "../data/fiscal_incentive.json"

rows_df_time = []

for iii in range(1, 50):
    #PARAMETROS DE LA CORRIDA - POR DEFECTO
    #lugar, por defecto providencia
    lugar_run  = "Providencia"
    #% área máxima respecto a original, 1 = 100%, el área no cambia, 0.8 significa que baja el 20%
    area_run = 1
    #tlpsp, 1 = 100%, es decir no cambia
    tlpsp_run = 1
    #demanda no abastecida, por defecto 5%
    nse_run = 0.05
    #costo energía desperdiciada, 1 = 100% = el mismo valor de instance data
    w_cost_run = 1
    #costo de combustible, 1 = 100% = el mismo valor de instance data
    fuel_cost_run = 1
    #demanda, 1 = 100% = el mismo valor del csv, 0.8 todo el csv baja el 80%
    demanda_run = 1
    #forecast viento, 1 = 100% = el mismo valor del csv, 0.8 todo el csv baja el 80%
    forecast_w_run = 1
    #forecast solar, 1 = 100% = el mismo valor del csv, 0.8 todo el csv baja el 80%
    forecast_s_run = 1
    #gap, por defecto 1%
    gap_run = 0.01
    #lista de restricciones que el modelo omitirá, por defecto siempre omite dieselsolar
    list_bypass_constraint_run = ['dieselsolar']
    #tamaño json de baterías, si se coloca por ejemplo 0.5 el json se reducirá en un 50%
    json_baterias_run = 1
    #tamaño json de diesel, si se coloca por ejemplo 0.5 el json se reducirá en un 50%
    json_diesel_run = 1
    #tamaño json solar, si se coloca por ejemplo 0.5 el json se reducirá en un 50%
    json_solar_run = 1
    #tamaño json eólico, si se coloca por ejemplo 0.5 el json se reducirá en un 50%
    json_wind_run = 1
    #longitud del horizonte temporal en %, 1 es igual, es decir 8760, 0.5 se reduciría a 4380
    htime_run = 1 
    #usar o no incentivo fiscal, binario, 1 sí, 0 no
    delta_run = 1
    #Variables auxiliares por si el horizonte temporal sube o baja y por si los json cambian de tamaño
    aumento_tiempo = "False"
    estado_json_d = "Igual"
    estado_json_s = "Igual"    
    estado_json_w = "Igual"
    estado_json_b = "Igual"
    #add_name es string que ayuda a ponerle el nombre a la instancia para que sea de fácil identificación
    add_name = ""
    
    
    #INSTANCIAS
    #colocar cuál instancia tendrá cada lugar diferente a Providencia
    instances_l = [1,2,3,4,5]
    instances_pn = [6,7,8,9,10]
    instances_sa = [11,12,13,14,15]
    instances_test = [16,17,18,19,20]
    if (iii in instances_l):
        lugar_run = "Leticia"
    elif (iii  in instances_pn):
        lugar_run = "Puerto Nariño"
    elif (iii  in instances_sa):
        lugar_run = "San Andrés"
    elif (iii in instances_test):
        lugar_run = "Test"
    
    #Espacio para escoger restricciones omitidas, se pueden poner más o combinar
    if (iii == 16):
        list_bypass_constraint_run = ['None']
        add_name = 'AllConstraints'
    elif (iii == 17):
        list_bypass_constraint_run = ['balance']
        add_name = 'NOTbalance'
    elif (iii == 18):
        list_bypass_constraint_run = ['G_mindiesel']
        add_name = 'NOTmindiesel'
    elif (iii == 19):
        list_bypass_constraint_run = ['Bconstraint3','Bconstraint4']
        add_name = 'NOTb34'
    elif (iii == 20):
        list_bypass_constraint_run = ['Bconstraint5','Bconstraint6']
        add_name = 'NOTb56'
    elif (iii == 21):
        list_bypass_constraint_run = ['bcbd']
        add_name = 'NOTbcbd'
    elif (iii == 22):
        list_bypass_constraint_run = ['other']
        add_name = 'NOTotherrule'
    elif (iii == 23):
        list_bypass_constraint_run = ['lpspcons']
        add_name = 'NOTlpsp'
    
    #crear un string con las restricciones omitidas para exportar los resultados
    bypass_constraint_run = ', '.join([str(item) for item in list_bypass_constraint_run])
    
    #instancias tlpsp
    if (iii == 13 or iii == 20 or iii == 33):
        tlpsp_run = 2
        add_name = '2tlpsp'
    elif (iii == 30):
        tlpsp_run = 3
        add_name = '3tlpsp'
    elif (iii == 31):
        tlpsp_run = 7
        add_name = '7tlpsp'
    elif (iii == 32):
        tlpsp_run = 24
        add_name = '24tlpsp'
    elif (iii == 34):
        tlpsp_run = 100
        add_name = '100tlpsp'
    
    #instancias área
    if (iii == 18):
        area_run = 0.8
        add_name = '80%area'
    elif (iii == 19):
        area_run = 0.9
        add_name = '90%area'
    elif (iii == 20):
        area_run = 1.1
        add_name = '110%area'
    elif (iii == 21):
        area_run = 1.2
        add_name = '120%area'
    elif (iii == 22):
        area_run = 1.3
        add_name = '130%area'
    
    #instancias wcost
    if (iii == 33):
        w_cost_run = 0.5
        add_name = '50%wcost'
    elif (iii == 34):
        w_cost_run = 0.9    
        add_name = '90%wcost'
    elif (iii == 36):
        w_cost_run = 1.1    
        add_name = '110%wcost'
    elif (iii == 37):
        w_cost_run = 1.5
        add_name = '150%wcost'
    
    #istancias demanda sube o baja
    if (iii == 48 or iii == 50):
        demand_run = 0.5
        add_name = '50%demand'
    elif (iii == 40 or iii == 5):
        demand_run = 0.9  
        add_name = '90%demand'
    elif (iii == 1 or iii == 6):
        demand_run = 1.1 
        add_name = '110%demand'
    elif (iii == 2):
        demand_run = 1.3
        add_name = '130%demand'
    elif (iii == 49):
        demand_run = 1.5
        add_name = '150%demand'
    
    #instancias forecast wt
    if (iii == 3):
        forecast_w_run = 0.5
        add_name = '50%wt'
    elif (iii == 4):
        forecast_w_run = 0.9
        add_name = '90%wt'
    elif (iii == 6):
        forecast_w_run = 1.1
        add_name = '110%wt'

        
    #instancias forecast solar
    if (iii == 3):
        forecast_s_run = 0.5
        add_name = '50%DNI'
    elif (iii == 4):
        forecast_s_run = 0.9
        add_name = '90%DNI'
    elif (iii == 7):
        forecast_s_run = 1.1
        add_name = '110%DNI'
    elif (iii == 8):
        forecast_s_run = 1.5
        add_name = '150%DNI'


    #instancias gap
    if (iii == 10):
        gap_run == 0.001
        add_name = '0.1%GAP'
    elif (iii == 11):
        gap_run == 0.005
        add_name = '0.5%GAP'
    elif (iii == 12):
        gap_run == 0.02
        add_name = '2%GAP'
    elif (iii == 13):
        gap_run == 0.03
        add_name = '3%GAP'
    elif (iii == 14):
        gap_run == 0.05
        add_name = '5%GAP'
    elif (iii == 15):
        gap_run == 0.1
        add_name = '10%GAP'
    elif (iii == 16):
        gap_run == 0
        add_name = '0%GAP'
        
    #instancias cambios en el tamaño del json
    if (iii == 10):
        #todos cambian de tamaño
        add_name = '50%json'
        json_baterias_run = 0.5
        estado_json_b = "Baja"
        json_diesel_run = 0.5
        estado_json_d = "Baja"
        json_solar_run = 0.5
        estado_json_s = "Baja"
        json_wind_run = 0.5
        estado_json_w = "Baja"                   
    elif (iii == 11):
        add_name = '120%json'
        json_baterias_run = 1.2
        estado_json_b = "Sube"
        json_diesel_run = 1.2
        estado_json_d = "Sube"
        json_solar_run = 1.2
        estado_json_s = "Sube"
        json_wind_run = 1.2
        estado_json_w = "Sube"         
        
    elif (iii == 12):
        #solo la batería cambia de tamaño
        add_name = '150%jsonb'
        json_baterias_run = 1.5
        estado_json_b = "Sube"
    elif (iii == 15):
        add_name = '80%jsonb'
        json_baterias_run = 0.8
        estado_json_b = "Baja"
    elif (iii == 13):
        add_name = '50%jsonw'
        json_wind_run = 0.5
        estado_json_w = "Baja"  

    #instancias cambio tamaño horizonte temporal
    if (iii == 13):
        aumento_tiempo = "True"
        add_name = '150%htime'
        htime_run = 1.5
    elif (iii == 14):
        aumento_tiempo = "True"
        htime_run = 1.2
        add_name = '120%htime'
    elif (iii == 15):
        htime_run = 0.8
        add_name = '80%htime'
    elif (iii == 16):
        htime_run = 0.5
        add_name = '50%htime'   
    
    #cargar datos    
    if (lugar_run == "San Andrés"):
        demand_filepath = demand_filepath_sa
        forecast_filepath = forecast_filepath_sa
        units_filepath = units_filepath_sa
        instanceData_filepath = instanceData_filepath_sa
    elif (lugar_run == "Providencia"):
        demand_filepath = demand_filepath_p
        forecast_filepath = forecast_filepath_p
        units_filepath = units_filepath_p
        instanceData_filepath = instanceData_filepath_p
    elif (lugar_run == "Leticia"):
        demand_filepath = demand_filepath_l
        forecast_filepath = forecast_filepath_l
        units_filepath = units_filepath_l
        instanceData_filepath = instanceData_filepath_l
    elif (lugar_run == "Puerto Nariño"):
        demand_filepath = demand_filepath_pn
        forecast_filepath = forecast_filepath_pn
        units_filepath = units_filepath_pn
        instanceData_filepath = instanceData_filepath_pn
    else:
        demand_filepath = demand_filepath_test
        forecast_filepath = forecast_filepath_test
        units_filepath = units_filepath_test
        instanceData_filepath = instanceData_filepath_test
    
    
    
    
    time_i_create_data = time.time() #initial time
    time_i_total = time.time()
    
    # read data general
    demand_df_fix, forecast_df_fix, generators_total, batteries_total, instance_data, fisc_data = read_data(demand_filepath,
                                                                                                            forecast_filepath,
                                                                                                            units_filepath,
                                                                                                            instanceData_filepath,
                                                                                                            fiscalData_filepath)
    
    
    len_total_time = len(demand_df_fix)
    
    #crear dataframe del tamaño colocado
    if (aumento_tiempo == "False"):
        demand_df = copy.deepcopy(demand_df_fix.head(len_total_time * htime_run))
        forecast_df = copy.deepcopy(forecast_df_fix.head(len_total_time * htime_run))
    else:
        aux_demand = copy.deepcopy(demand_df_fix)
        aux_forecast = copy.deepcopy(forecast_df_fix)
        #si aumenta el tamaño se coloca aleatoriamente datos hasta completar el valor faltante
        mean_demand = aux_demand['demand'].mean()
        desvest_demand = aux_demand['demand'].std()
        mean_wt = aux_forecast['Wt'].mean()
        desvest_wt = aux_forecast['Wt'].std()        
        mean_dni = aux_forecast['DNI'].mean()
        desvest_dni = aux_forecast['DNI'].std()        
        count = len(aux_demand)
        
        #empezar a llenar los datos de forecast y demanda
        for i in range(int(len_total_time * (htime_run - 1))):
            insert_demand = np.random.normal(loc=mean_demand, scale=desvest_demand, size=1)
            insert_wt = np.random.normal(loc=mean_wt, scale=desvest_wt, size=1)
            insert_dni = np.random.normal(loc=mean_dni, scale=desvest_dni, size=1)
            numero_demand = int(insert_demand[0])
            numero_wt = int(insert_wt[0])
            numero_dni = int(insert_dni[0])
            
            aux_demand.append({'t':count,'demand': numero_demand}, ignore_index = True)
            aux_forecast.append({'t':count, 'DNI':numero_dni, 't_ambt':0, 'Wt': numero_wt, 'Qt':0},ignore_index = True)
            
            count = count + 1
            
        demand_df = copy.deepcopy (aux_demand)
        forecast_df = copy.deepcopy (aux_forecast)
        
        
    #multiplicar por si hay reducción o aumento
    parameter_demand = demanda_run * instance_data['demand_covered']
    demand_df['demand'] = parameter_demand  * demand_df['demand'] 
    forecast_df['Wt'] = forecast_w_run * forecast_df['Wt'] 
    forecast_df['DNI'] = forecast_s_run * forecast_df['DNI']
    
    
    default_batteries = copy.deepcopy(batteries_total)
    default_diesel = []
    default_solar = []
    default_wind = []
    
    #definir la misma semilla para que los random siempre den lo mismo
    random.seed(42)
    #saber la tecnología de cada generador
    for i in generators_total:
        if (i['tec'] == 'D'):
            default_diesel.append(i)
        elif (i['tec'] == 'S'):
            default_solar.append(i)
        elif (i['tec'] == 'W'):
            default_wind.append(i)
    
    #crear los datos según el tamaño establecido
    if (estado_json_d == "Baja"):
        default_diesel = random.sample(default_diesel, int(len(default_diesel) * json_diesel_run))
    elif (estado_json_d == "Sube"):
        aux_default_diesel = copy.deepcopy(default_diesel)
        count_d = 1
        #si aumenta llenar con datos que ya tiene, escoger uno aleatorio y unir al df
        for i in range(int(len(default_diesel)*(json_diesel_run - 1))):
            random_diesel = []
            random_diesel = random.choice(aux_default_diesel)
            random_diesel['id_gen'] = 'Diesel_new' + str(count_d)
            aux_default_diesel.append(random_diesel)
            count_d = count_d + 1
            
        default_diesel = copy.deepcopy(aux_default_diesel)
            

    if (estado_json_s == "Baja"):
        default_solar = random.sample(default_solar, int(len(default_solar) * json_solar_run))
    elif (estado_json_s == "Sube"):
        aux_default_solar = copy.deepcopy(default_solar)
        count_s = 1
        for i in range(int(len(default_solar)*(json_solar_run - 1))):
            random_solar = []
            random_solar = random.choice(aux_default_solar)
            random_solar['id_gen'] = 'Solar_new' + str(count_s)
            aux_default_solar.append(random_solar)
            count_s = count_s + 1
            
        default_solar = copy.deepcopy(aux_default_solar)            
            
    if (estado_json_w == "Baja"):
        default_wind = random.sample(default_wind, int(len(default_wind) * json_wind_run))
    elif (estado_json_w == "Sube"):
        aux_default_wind = copy.deepcopy(default_wind)
        count_w = 1
        for i in range(int(len(default_wind)*(json_wind_run - 1))):
            random_wind = []
            random_wind = random.choice(aux_default_wind)
            random_wind['id_gen'] = 'Wind_new' + str(count_w)
            aux_default_wind.append(random_wind)
            count_w = count_w + 1
            
        default_wind = copy.deepcopy(aux_default_wind)  

    if (estado_json_b == "Baja"):
        default_batteries = random.sample(default_batteries, int(len(default_batteries) * json_baterias_run))
    elif (estado_json_b == "Sube"):
        aux_default_batteries = copy.deepcopy(default_batteries)
        count_b = 1
        for i in range(int(len(default_batteries)*(json_baterias_run - 1))):
            random_batteries = []
            random_batteries = random.choice(aux_default_batteries)
            random_batteries['id_bat'] = 'Batterie_new' + str(count_b)
            aux_default_batteries.append(random_batteries)
            count_b = count_b + 1
            
        default_batteries = copy.deepcopy(aux_default_batteries)  


    
    generators = default_diesel + default_solar + default_wind
    batteries = default_batteries
    nse_run = instance_data['nse']
    
    #instancias nse diferente a por defecto
    if (iii == 23):
        nse_run = 0.001
        add_name = '0.1%nse'
    elif (iii == 24):
        nse_run = 0.01
        add_name = '1%nse'
    elif (iii == 25):
        nse_run = 0.02
        add_name = '2%nse'
    elif (iii == 26):
        add_name = '3%nse'
        nse_run = 0.03
    elif (iii == 27):
        add_name = '5%nse'
        nse_run = 0.05

    
    #Max datos
    maxtec = instance_data['maxtec'] 
    mintec = instance_data['mintec'] 
    maxbr = instance_data['max_brand']
    
    if (iii == 10):
        maxtec = 2
        add_name = 'maxtec2'
 
    
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
    
    if (delta_run == 0):
        delta = 1
    
    amax = instance_data['amax'] * area_run
    time_f_create_data = time.time() - time_i_create_data #final time create
    
    time_i_make_model = time.time()
    # Create model          
    model = opt.make_model(generators_dict, 
                           batteries_dict, 
                           dict(zip(demand_df.t, demand_df.demand)),
                           technologies_dict, 
                           renewables_dict, 
                           amax =  amax, 
                           fuel_cost =  instance_data['fuel_cost'] * fuel_cost_run,
                           ir = ir, 
                           nse = nse_run, 
                           maxtec = maxtec, 
                           mintec = mintec, 
                           maxbr = maxbr,
                           years = instance_data['years'],
                           w_cost = instance_data['w_cost']*w_cost_run,
                           tlpsp = tlpsp_run,
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
       #plot(generation_graph)
       try:
           percent_df, energy_df, renew_df, total_df, brand_df = calculate_energy(batteries_dict, generators_dict, model_results, demand_df)
       except KeyError:
           pass
    
    time_f_results = time.time() - time_i_results
    time_f_total = time.time() - time_i_total
    
    name_esc = 'esc_' + str(iii) + ' ' + str(lugar_run) + ' ' + ' ' + str(add_name)
    rows_df_time.append([iii,name_esc, lugar_run, amax, tlpsp_run, nse_run, 
                        instance_data['w_cost']*w_cost_run,len(demand_df),demanda_run, forecast_w_run,forecast_s_run,
                        gap_run, len(default_batteries), len(default_diesel),
                        len(default_solar),len(default_wind), bypass_constraint_run,
                        time_f_total, time_f_create_data, time_f_results, time_f_solve, time_f_make_model])    

#dataframe completo con todas las instancias
df_time = pd.DataFrame(rows_df_time, columns=["N", "Name", "City","Area","Tlpsp",
                                              "NSE", "W_cost", "Len_demand","demand percent", "Forecast_wind",
                                              "Forecast_solar","gap","json batteries", "json diesel",
                                              "json solar", "json wind","excluded constraints",
                                              "TOTAL TIME","CREATE DATA TIME", "RESULTS TIME","SOLVE TIME",
                                              "MAKE MODEL TIME"])

#crear Excel
def multiple_dfs(df_list, sheets, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)   
        row = row + 1
    writer.save()

# list of dataframes
dfs = [df_time]

# run function
multiple_dfs(dfs, 'ExecTime', 'Total_instances.xlsx')


'''
TRM = 3910
LCOE_COP = TRM * model_results.descriptive['LCOE']
model_results.df_results.to_excel("results.xlsx") 
'''
