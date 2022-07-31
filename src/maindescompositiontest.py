# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:14:21 2022

@author: pmayaduque
"""
from utilities import read_data, create_objects, calculate_sizingcost, create_technologies, calculate_area, calculate_energy, interest_rate
from utilities import fiscal_incentive
import opttest as opt
import pandas as pd 
from operators_test import Sol_constructor, Search_operator
from plotly.offline import plot
import copy
import time
import numpy as np
import random
pd.options.display.max_columns = None

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

for iii in range(1, 137):
    #PARAMETROS DE LA CORRIDA - POR DEFECTO
    #lugar
    lugar_run  = "Providencia"
    #iteraciones
    iteraciones_run = 30
    #area, por defecto 100%
    area_run = 1
    #%probabilidad escoger cada tecnología, por defecto 25% cada una
    d_p_run = 0.25
    s_p_run = 0.25
    w_p_run = 0.25
    b_p_run = 0.25
    #tlpsp, por defecto 1
    tlpsp_run = 1
    #nse, por defecto 5%
    nse_run = 0.05
    #%wcost, por defecto 100%
    w_cost_run = 1
    #%sube o baja fuel cost, por defecto 100% es decir el mismo valor
    fuel_cost_run = 1
    #%demanda, por defecto 100%
    demanda_run = 1
    #%forectrast viento, por defecto 100%
    forecast_w_run = 1
    #%forecast solar, por defecto 100%
    forecast_s_run = 1
    #gap, por defecto 1%
    gap_run = 0.01
    #lista de restricciones que se omitirán
    list_bypass_constraint_run = ['dieselsolar']
    #método de añadir, grasp o random
    add_function_run = "Grasp"
    #tamaño de los json, 1 = 100%, 50% se reduciría su tamaño a la mitad
    json_baterias_run = 1
    json_diesel_run = 1
    json_solar_run = 1
    json_wind_run = 1
    htime_run = 1 
    #binario incentivo fiscal, 1 sí se usa, 0 no
    delta_run = 1
    #variables auxiliares
    aumento_tiempo = "False"
    estado_json_d = "Igual"
    estado_json_s = "Igual"    
    estado_json_w = "Igual"
    estado_json_b = "Igual"
    #string para poner el nombre al escenario
    add_name = ""
    
    
    #INSTANCIAS
    #instancias que llevan lugares diferentes a providencia
    instances_l = [1,9,10,11,12,85,86,87,88,89,90,91]
    instances_pn = [3,53,54,55,56,57,63,64,65,66,67,73,74,75,76,77]
    instances_sa = [4,5,6,7,8,104,106]
    if (iii in instances_l):
        lugar_run = "Leticia"
    elif (iii  in instances_pn):
        lugar_run = "Puerto Nariño"
    elif (iii  in instances_sa):
        lugar_run = "San Andrés"
    
    #instancias con iteraciones diferentes a 30
    instances_iterations_40 = [5,6,7,8,9,10,11,12,13,14,15,16,17,41,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102]
    instances_iterations_50 = [1,2,3,4,42]
    
    if (iii in instances_iterations_40):
        iteraciones_run = 40
    elif (iii in instances_iterations_50):
        iteraciones_run = 50
    elif (iii == 38):
        iteraciones_run = 10
    elif (iii == 39):
        iteraciones_run = 20
    elif (iii == 40):
        iteraciones_run = 30        
    elif (iii == 43):
        iteraciones_run = 60
    elif (iii == 44):
        iteraciones_run = 70        
    elif (iii == 45):
        iteraciones_run = 80        
    elif (iii == 46):
        iteraciones_run = 90        
    elif (iii == 47):
        iteraciones_run = 100        
    
    
    #instancias con restricciones omitidas
    if (iii == 92):
        list_bypass_constraint_run = ['None']
        add_name = 'AllConstraints'
    elif (iii == 94):
        list_bypass_constraint_run = ['balance']
        add_name = 'NOTbalance'
    elif (iii == 95):
        list_bypass_constraint_run = ['G_mindiesel']
        add_name = 'NOTmindiesel'
    elif (iii == 96):
        list_bypass_constraint_run = ['Bconstraint3','Bconstraint4']
        add_name = 'NOTb34'
    elif (iii == 97):
        list_bypass_constraint_run = ['Bconstraint5','Bconstraint6']
        add_name = 'NOTb56'
    elif (iii == 98):
        list_bypass_constraint_run = ['bcbd']
        add_name = 'NOTbcbd'
    elif (iii == 99 or iii == 100):
        list_bypass_constraint_run = ['other']
        add_name = 'NOTotherrule'
    elif (iii == 102):
        list_bypass_constraint_run = ['lpspcons']
        add_name = 'NOTlpsp'

        
        
        
    #string para exportar los datos de las restricciones omitidas
    bypass_constraint_run = ', '.join([str(item) for item in list_bypass_constraint_run])

    #instancias con diferente probabilidad de añadir una tecnología
    if(iii == 5 or iii == 9):
        b_p_run == 0.5
        add_name = '50%bat'
    elif(iii == 6 or iii == 10):
        d_p_run == 0.5
        add_name = '50%diesel'
    elif(iii == 7 or iii == 11):
        w_p_run == 0.5
        add_name = '50%wind'
    elif(iii == 8 or iii == 12):
        s_p_run == 0.5
        add_name = '50%solar'

    #instancias tlpsp
    if (iii == 13 or iii == 100 or iii == 101):
        tlpsp_run = 2
        add_name = '2tlpsp'
    elif (iii == 14):
        tlpsp_run = 3
        add_name = '3tlpsp'
    elif (iii == 15):
        tlpsp_run = 7
        add_name = '7tlpsp'
    elif (iii == 16):
        tlpsp_run = 24
        add_name = '24tlpsp'
    elif (iii == 17):
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
    
    #istancias demanda
    if (iii == 48 or iii == 53):
        demand_run = 0.5
        add_name = '50%demand'
    elif (iii == 49 or iii == 54):
        demand_run = 0.9  
        add_name = '90%demand'
    elif (iii == 51 or iii == 56):
        demand_run = 1.1 
        add_name = '110%demand'
    elif (iii == 52):
        demand_run = 1.3
        add_name = '130%demand'
    elif (iii == 57):
        demand_run = 1.5
        add_name = '150%demand'


    #instancias forecast wt
    if (iii == 58 or iii == 63):
        forecast_w_run = 0.5
        add_name = '50%wt'
    elif (iii == 59 or iii == 64):
        forecast_w_run = 0.9
        add_name = '90%wt'
    elif (iii == 61 or iii == 66):
        forecast_w_run = 1.1
        add_name = '110%wt'
    elif (iii == 62 or iii == 67):
        forecast_w_run = 1.5
        add_name = '150%wt'
        
    #instancias forecast solar
    if (iii == 68 or iii == 73):
        forecast_s_run = 0.5
        add_name = '50%DNI'
    elif (iii == 69 or iii == 74):
        forecast_s_run = 0.9
        add_name = '90%DNI'
    elif (iii == 71 or iii == 76):
        forecast_s_run = 1.1
        add_name = '110%DNI'
    elif (iii == 72 or iii == 77):
        forecast_s_run = 1.5
        add_name = '150%DNI'


    #instancias gap
    if (iii == 78 or iii == 85):
        gap_run == 0.001
        add_name = '0.1%GAP'
    elif (iii == 79 or iii == 86):
        gap_run == 0.005
        add_name = '0.5%GAP'
    elif (iii == 80 or iii == 87):
        gap_run == 0.02
        add_name = '2%GAP'
    elif (iii == 81 or iii == 88):
        gap_run == 0.03
        add_name = '3%GAP'
    elif (iii == 82 or iii == 89):
        gap_run == 0.05
        add_name = '5%GAP'
    elif (iii == 83 or iii == 90):
        gap_run == 0.1
        add_name = '10%GAP'
    elif (iii == 84 or iii == 91):
        gap_run == 0
        add_name = '0%GAP'

    #instancias add o grasp
    if (iii == 105 or iii == 106):
        add_function_run = "random"
        add_name = 'Random'
        
    #instancias cambios en el tamaño del json
    if (iii == 107):
        add_name = '50%json'
        json_baterias_run = 0.5
        estado_json_b = "Baja"
        json_diesel_run = 0.5
        estado_json_d = "Baja"
        json_solar_run = 0.5
        estado_json_s = "Baja"
        json_wind_run = 0.5
        estado_json_w = "Baja"        
    elif (iii == 108):
        add_name = '80%json'
        json_baterias_run = 0.8
        estado_json_b = "Baja"
        json_diesel_run = 0.8
        estado_json_d = "Baja"
        json_solar_run = 0.8
        estado_json_s = "Baja"
        json_wind_run = 0.8
        estado_json_w = "Baja"             
    elif (iii == 110):
        add_name = '120%json'
        json_baterias_run = 1.2
        estado_json_b = "Sube"
        json_diesel_run = 1.2
        estado_json_d = "Sube"
        json_solar_run = 1.2
        estado_json_s = "Sube"
        json_wind_run = 1.2
        estado_json_w = "Sube"         
    elif (iii == 111):
        add_name = '150%json'
        json_baterias_run = 1.5
        estado_json_b = "Sube"
        json_diesel_run = 1.5
        estado_json_d = "Sube"
        json_solar_run = 1.5
        estado_json_s = "Sube"
        json_wind_run = 1.5
        estado_json_w = "Sube"     
    elif (iii == 112):
        add_name = '150%jsonb'
        json_baterias_run = 1.5
        estado_json_b = "Sube"
    elif (iii == 113):
        add_name = '120%jsonb'
        json_baterias_run = 1.2
        estado_json_b = "Sube" 
    elif (iii == 115):
        add_name = '80%jsonb'
        json_baterias_run = 0.8
        estado_json_b = "Baja"
    elif (iii == 116):
        add_name = '50%jsonb'
        json_baterias_run = 0.5
        estado_json_b = "Baja"
    elif (iii == 117):
        add_name = '150%jsond'
        json_diesel_run = 1.5
        estado_json_d = "Sube"
    elif (iii == 118):
        add_name = '120%jsond'
        json_diesel_run = 1.2
        estado_json_d = "Sube" 
    elif (iii == 120):
        add_name = '80%jsond'
        json_diesel_run = 0.8
        estado_json_d = "Baja"
    elif (iii == 121):
        add_name = '50%jsond'
        json_diesel_run = 0.5
        estado_json_d = "Baja"        
    elif (iii == 122):
        add_name = '150%jsons'
        json_solar_run = 1.5
        estado_json_s = "Sube"
    elif (iii == 123):
        add_name = '120%jsons'
        json_solar_run = 1.2
        estado_json_s = "Sube" 
    elif (iii == 125):
        add_name = '80%jsons'
        json_solar_run = 0.8
        estado_json_s = "Baja"
    elif (iii == 126):
        add_name = '50%jsons'
        json_solar_run = 0.5
        estado_json_s = "Baja"      
    elif (iii == 127):
        add_name = '150%jsonw'
        json_wind_run = 1.5
        estado_json_w = "Sube"
    elif (iii == 128):
        add_name = '120%jsonw'
        json_wind_run = 1.2
        estado_json_w = "Sube" 
    elif (iii == 130):
        add_name = '80%jsonw'
        json_wind_run = 0.8
        estado_json_w = "Baja"
    elif (iii == 131):
        add_name = '50%jsonw'
        json_wind_run = 0.5
        estado_json_w = "Baja"  

    #instancias cambio tamaño horizonte temporal
    if (iii == 132):
        aumento_tiempo = "True"
        add_name = '150%htime'
        htime_run = 1.5
    elif (iii == 133):
        aumento_tiempo = "True"
        htime_run = 1.2
        add_name = '120%htime'
    elif (iii == 135):
        htime_run = 0.8
        add_name = '80%htime'
    elif (iii == 136):
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
    # read data
    demand_df_fix, forecast_df_fix, generators_total, batteries_total, instance_data, fisc_data = read_data(demand_filepath,
                                                                                                            forecast_filepath,
                                                                                                            units_filepath,
                                                                                                            instanceData_filepath,
                                                                                                            fiscalData_filepath)
    
    
    len_total_time = len(demand_df_fix)
    
    #crear dataframe del tamaño colocado
    if (aumento_tiempo == "False"):
        demand_df = copy.deepcopy(demand_df_fix.head(int(len_total_time * htime_run)))
        forecast_df = copy.deepcopy(forecast_df_fix.head(int(len_total_time * htime_run)))
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
    elif (iii == 28):
        add_name = '8%nse'
        nse_run = 0.08
    elif (iii == 29):
        add_name = '10%nse'
        nse_run = 0.1
    elif (iii == 30):
        add_name = '15%nse'
        nse_run = 0.15
    elif (iii == 31):
        add_name = '20%nse'
        nse_run = 0.2
    elif (iii == 32):
        add_name = '30%nse'
        nse_run = 0.3

                      
        
        
    #Calculate interest rate
    ir = interest_rate(instance_data['i_f'],instance_data['inf'])
    #Calculate CRF
    CRF = (ir * (1 + ir)**(instance_data['years']))/((1 + ir)**(instance_data['years'])-1)  
    
    #Set solver settings
    MIP_GAP = gap_run
    TEE_SOLVER = True
    OPT_SOLVER = 'gurobi'
    SEED_R = 42
    np.random.seed(SEED_R)
    
    #Calculate fiscal incentives
    delta = fiscal_incentive(fisc_data['credit'], 
                             fisc_data['depreciation'],
                             fisc_data['corporate_tax'],
                             ir,
                             fisc_data['T1'],
                             fisc_data['T2'])
    
    if (delta_run == 0):
        delta = 1
    
    # Create objects and generation rule
    generators_dict, batteries_dict,  = create_objects(generators,
                                                       batteries,  
                                                       forecast_df,
                                                       demand_df,
                                                       instance_data)
    #create technologies
    technologies_dict, renewables_dict = create_technologies (generators_dict,
                                                              batteries_dict)
    
    
    time_f_create_data = time.time() - time_i_create_data #final time create
    
    time_i_firstsol = time.time()
    #create the initial solution operator
    sol_constructor = Sol_constructor(generators_dict, 
                                batteries_dict,
                                demand_df,
                                forecast_df)
    
    #auxiliar diccionario para evitar borrar datos
    aux_instance_data = copy.deepcopy(instance_data)
    aux_instance_data['amax'] = aux_instance_data['amax'] * area_run
    aux_instance_data['tlpsp'] = tlpsp_run
    aux_instance_data['nse'] = nse_run 
    aux_instance_data['w_cost'] = w_cost_run * aux_instance_data['w_cost'] 
    aux_instance_data['fuel_cost'] = aux_instance_data['fuel_cost'] * fuel_cost_run
    
    
    #create a default solution
    sol_feasible = sol_constructor.initial_solution(aux_instance_data,
                                                   generators_dict, 
                                                   batteries_dict, 
                                                   technologies_dict, 
                                                   renewables_dict,
                                                   delta,
                                                   OPT_SOLVER,
                                                   MIP_GAP,
                                                   TEE_SOLVER,
                                                   list_bypass_constraint_run)
    
    
    time_f_firstsol = time.time() - time_i_firstsol #final time
    # set the initial solution as the best so far
    sol_best = copy.deepcopy(sol_feasible)
    
    # create the actual solution with the initial soluion
    sol_current = copy.deepcopy(sol_feasible)
    
    #check the available area
    
    #nputs for the model
    movement = "Initial Solution"
    amax =  instance_data['amax'] * area_run
    N_iterations = instance_data['N_iterations']
    #df of solutions
    rows_df = []
    
    # Create search operator
    search_operator = Search_operator(generators_dict, 
                                batteries_dict,
                                demand_df,
                                forecast_df)
    
    
    dict_time_iter = {}
    dict_time_remove = {}
    dict_time_add = {}
    dict_time_make = {}
    dict_time_solve = {}
    time_i_iterations = time.time()
    #si no es factible la solución inicial no hacer nada
    if (sol_feasible.results != None):
        for i in range(int(iteraciones_run)):
                
            time_i_range = time.time()
            rows_df.append([i, sol_current.feasible, 
                            sol_current.results.descriptive['area'], 
                            sol_current.results.descriptive['LCOE'], 
                            sol_best.results.descriptive['LCOE'], movement])
            if sol_current.feasible == True:     
                # save copy as the last solution feasible seen
                sol_feasible = copy.deepcopy(sol_current) 
                # Remove a generator or battery from the current solution
                time_i_remove = time.time()
                sol_try, dic_remove = search_operator.removeobject(sol_current, CRF)
                time_f_remove = time.time() - time_i_remove #final time
                dict_time_remove[i] = time_f_remove
                movement = "Remove"
            else:
                #  Create list of generators that could be added
                list_available_bat, list_available_gen, list_tec_gen  = search_operator.available(sol_current, amax)
                if (list_available_gen != [] or list_available_bat != []):
                    # Add a generator or battery to the current solution
                    time_i_add = time.time()
                    #aumentar la probabilidad de list si se establece, colocando más peso
                    if (b_p_run == 0.5 and list_available_bat != []):
                        list_tec_gen = list_tec_gen + ['B','B']
                    if((w_p_run == 0.5) and (list_available_gen != []) and ('W' in  list_tec_gen)):
                       list_tec_gen = list_tec_gen + ['W','W']
                    if((s_p_run == 0.5) and (list_available_gen != []) and ('S' in  list_tec_gen)):
                       list_tec_gen = list_tec_gen + ['S','S']
                    if((d_p_run == 0.5) and (list_available_gen != []) and ('D' in  list_tec_gen)):
                       list_tec_gen = list_tec_gen + ['D','D']                    
                        
                    #escoger cuál función usar
                    if (add_function_run == "random"):
                        sol_try = search_operator.addrandomobject(sol_current, list_available_bat, list_available_gen, list_tec_gen)
                    else:
                        sol_try, dic_remove = search_operator.addobject(sol_current, list_available_bat, list_available_gen, list_tec_gen, dic_remove,  CRF, instance_data['fuel_cost'])
        
                    movement = "Add"
                    time_f_add = time.time() - time_i_add #final time
                    dict_time_add[i] = time_f_add
                else:
                    # return to the last feasible solution
                    sol_current = copy.deepcopy(sol_feasible)
                    continue # Skip running the model and go to the begining of the for loop
            
            #si no hay nada poner uno aleatorio para evitar errores
            if (sol_try.generators_dict_sol == {} and sol_try.batteries_dict_sol == {}):
                select_ob = random.choice(list(generators_dict.keys()))
                sol_try.generators_dict_sol[select_ob] = generators_dict[select_ob]
                
            tnpccrf_calc = calculate_sizingcost(sol_try.generators_dict_sol, 
                                                sol_try.batteries_dict_sol, 
                                                ir = ir,
                                                years = instance_data['years'],
                                                delta = delta)
            time_i_make = time.time()
            model = opt.make_model_operational(generators_dict = sol_try.generators_dict_sol,
                                               batteries_dict = sol_try.batteries_dict_sol,  
                                               demand_df=dict(zip(demand_df.t, demand_df.demand)), 
                                               technologies_dict = sol_try.technologies_dict_sol,  
                                               renewables_dict = sol_try.renewables_dict_sol,
                                               fuel_cost =  instance_data['fuel_cost'] * fuel_cost_run,
                                               nse =  nse_run, 
                                               TNPCCRF = tnpccrf_calc,
                                               w_cost = instance_data['w_cost'] * w_cost_run,
                                               tlpsp = tlpsp_run,
                                               bypass = list_bypass_constraint_run) 
            
            time_f_make = time.time() - time_i_make
            dict_time_make[i] = time_f_make
            time_i_solve = time.time()
            results, termination = opt.solve_model(model, 
                                                   optimizer = OPT_SOLVER,
                                                   mipgap = MIP_GAP,
                                                   tee = TEE_SOLVER)
            time_f_solve = time.time() - time_i_solve
            dict_time_solve[i] = time_f_solve
        
        
            if termination['Temination Condition'] == 'optimal':
                sol_try.results.descriptive['LCOE'] = model.LCOE_value.expr()
                sol_try.results = opt.Results(model)
                sol_try.feasible = True
                sol_current = copy.deepcopy(sol_try)
                if sol_try.results.descriptive['LCOE'] <= sol_best.results.descriptive['LCOE']:
                    sol_best = copy.deepcopy(sol_try)
            else:
                sol_try.feasible = False
                sol_try.results.descriptive['LCOE'] = None
                sol_current = copy.deepcopy(sol_try)
        
            sol_current.results.descriptive['area'] = calculate_area(sol_current)
            
            time_f_range = time.time() - time_i_range
            dict_time_iter[i] = time_f_range    
            #print(sol_current.generators_dict_sol)
            #print(sol_current.batteries_dict_sol)
                       
        time_f_iterations = time.time() - time_i_iterations #final time
        #df with the feasible solutions
        df_iterations = pd.DataFrame(rows_df, columns=["i", "feasible", "area", "LCOE_actual", "LCOE_Best","Movement"])
        
        time_i_results = time.time()
        #print results best solution
        print(sol_best.results.descriptive)
        print(sol_best.results.df_results)
        generation_graph = sol_best.results.generation_graph()
        #plot(generation_graph)
        try:
            percent_df, energy_df, renew_df, total_df, brand_df = calculate_energy(sol_best.batteries_dict_sol, sol_best.generators_dict_sol, sol_best.results, demand_df)
        except KeyError:
            pass
        time_f_results = time.time() - time_i_results
        time_f_total = time.time() - time_i_total #final time
        
        
        
        #calcular promedios de las iteraciones
        df_time_iter = pd.DataFrame(dict_time_iter.items(), columns = ['Iteration', 'Total iteration time']) 
        time_iter_average = df_time_iter['Total iteration time'].mean()
        df_time_solve = pd.DataFrame(dict_time_solve.items(), columns = ['Iteration', 'Solver time']) 
        time_solve_average = df_time_solve['Solver time'].mean()
        df_time_make = pd.DataFrame(dict_time_make.items(), columns = ['Iteration', 'make model time'])
        time_make_average = df_time_make['make model time'].mean()
        df_time_remove = pd.DataFrame(dict_time_remove.items(), columns = ['Iteration', 'Remove function time']) 
        time_remove_average = df_time_remove['Remove function time'].mean()
        df_time_add = pd.DataFrame(dict_time_add.items(), columns = ['Iteration', 'Add function time']) 
        time_add_average = df_time_add['Add function time'].mean()
        
        #crear fila del dataframe
        name_esc = 'esc_' + str(iii) + ' ' + str(lugar_run) + ' ' + str(iteraciones_run) + ' ' + str(add_name)
        rows_df_time.append([iii,name_esc, lugar_run, iteraciones_run, amax, tlpsp_run, nse_run, 
                            aux_instance_data['w_cost'],len(demand_df),demanda_run, forecast_w_run,forecast_s_run,
                            gap_run, add_function_run, len(default_batteries), len(default_diesel),
                            len(default_solar),len(default_wind), bypass_constraint_run,b_p_run, d_p_run, s_p_run,
                            w_p_run, time_f_total, time_f_create_data,time_f_firstsol, time_f_iterations,
                            time_iter_average, time_solve_average, time_make_average, time_remove_average,
                            time_add_average, time_f_results])    



#dataframe completo con todas las instancias
df_time = pd.DataFrame(rows_df_time, columns=["N", "Name", "City", "Iterations", "Area","Tlpsp",
                                              "NSE", "W_cost", "Len_demand","Demand percent", "Forecast_wind",
                                              "Forecast_solar","gap","add_function","json batteries", "json diesel",
                                              "json solar", "json wind","excluded constraints",
                                              "probability add batteries","probability add diesel",
                                              "probability add solar","probability add wind","TOTAL TIME",
                                              "CREATE DATA TIME", "FIRST SOLUTION TIME","ITERATIONS TIME",
                                              "ITERATIONS MEAN TIME","ITERATIONS MEAN SOLVER TIME",
                                              "ITERATIONS MEAN MAKE MODEL TIME","ITERATIONS REMOVE FUNCTION MEAN",
                                              "ITERATIONS ADD FUNCTION MEAN", "CREATE RESULTS TIME"])

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
def init_rng(seed):
    global rng
    rng = numpy.random.RandomState(seed=seed)



TRM = 3910
LCOE_COP = TRM * model_results.descriptive['LCOE']
sol_best.results.df_results.to_excel("results.xlsx") 
'''

