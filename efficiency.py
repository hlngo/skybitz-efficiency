# efficiency.py

import os, json
import pandas as pd  # panda's nickname is pd
import numpy as np  # numpy as np
from pandas import DataFrame, Series     # for convenience

THE_EXCEL_FILE = 'UWGTANKLIST.XLS' # The Export from ST List Page
REPORT_FORMAT = False # True if you want to read Report Generated format, False to read Tank List Export

# Functions
def set_the_excel_file(excelfilename):
    '''Sets the file string global var for use below'''
    THE_EXCEL_FILE = excelfilename

def read_excel():
    try:
        if REPORT_FORMAT:
            return pd.read_excel(THE_EXCEL_FILE, skiprows= 5) #skip first 5 rows for Reports output
        else:
            return pd.read_excel(THE_EXCEL_FILE) #direct Export from ST list page correctly gives headers as first row
    except:
        return {"Err" : "read error"}

def get_dataframe():
    eff = read_excel() #returns pd dataframe
    eff = eff[:-1] #drop last row 'Totals'
    return eff

def get_clean_dataframe():
    eff = read_excel() #returns pd dataframe
    eff = eff[:-1] #drop last row 'Totals'
    eff= eff.loc[(eff['Deliveries'] != 0)] #drop records with num deliveries 0
    return eff

def sanity_check():
    '''print simple pandas df summary using describe'''
    edf = get_clean_dataframe()
    print(edf.describe())

def get_total_actual_deliveries():
    '''Get the total actual deliveries made, return int'''
    edf = get_clean_dataframe()
    return edf['Deliveries'].sum()

def get_total_target_deliveries():
    '''Get the total suggested target deliveries, return int'''
    edf = get_clean_dataframe()
    return edf['Target Deliveries'].sum()

def get_deliveries_delta():
    '''Get the delta between target and actual deliveries'''
    return (get_total_actual_deliveries() - get_total_target_deliveries())

def get_delivery_efficiency():
    '''Get total delivery efficiency from delta of target and actual delivery count from all tanks, return int'''
    return round((get_total_target_deliveries() / get_total_actual_deliveries()), 3) * 100 #return as a percent

def get_total_actual_amt_delivered():
    '''Get total estimated amount delivered from sum of all tank averages, return int'''
    edf = get_clean_dataframe()
    # first we need to do some string formatting on the values and convert to numerics
    edf['Avg. Volume'] = edf['Avg. Volume'].str.strip(' gal')
    edf['Avg. Volume'] = pd.to_numeric(edf['Avg. Volume'].str.replace(',',''), errors='coerce')

    # then we can sum up the total from all of the averages
    total_avg_amt = edf['Avg. Volume'].sum()
    return total_avg_amt

def avg_amt_per_delivery():
    '''Get total estimated volume amount per delivery, return int'''
    return round((get_total_actual_amt_delivered() / get_total_actual_deliveries()), 1)

def get_total_delivery_target_amt():
    '''Get total target delivery amount from sum of all tank target amts, return int'''
    edf = get_clean_dataframe()
    # first we need to do some string formatting on the values and convert to numerics
    edf['Target Delivery Volume'] = edf['Target Delivery Volume'].str.strip(' gal')
    edf['Target Delivery Volume'] = pd.to_numeric(edf['Target Delivery Volume'].str.replace(',',''), errors='coerce')

    # then we can sum up the total from all of the averages
    total_avg_amt = edf['Target Delivery Volume'].sum()
    return total_avg_amt

def get_delivery_amt_efficiency():
    '''Get total delivery amount efficiency from delta of target and actual amt from all tanks, return int'''
    return round((get_total_actual_amt_delivered() / get_total_delivery_target_amt()), 3) * 100 #return as a percent

def get_total_potential_savings():
    '''Get the sum of potential savings for all tanks'''
    edf = get_clean_dataframe()
    # first, need to reformat strings, then convert to numeric
    edf['Potential Savings'] = pd.to_numeric(edf['Potential Savings'].str.replace('$',''), errors='coerce')
    return round(edf['Potential Savings'].sum(), 2) #sum, round and return

# Report Format Functions
def get_total_tank_count():
    '''Get the count of all tanks in report'''
    edf = get_dataframe()
    return len(edf)

def get_active_tank_count():
    '''Get the count of all active tanks in report'''
    edf = get_dataframe()
    return len(edf[(edf['Active'] == True)])

# Output and Write/Print Functions
def get_all_values_dict():
    '''Write the data values to json-formatted text for easy access from js'''
    data = dict(
        [
            ('total_actual_del', str(get_total_actual_deliveries())), #Total tank deliveries with at least 1 delivery
            ('total_amt_del', str(get_total_actual_amt_delivered())), #Total Amt Delivered from sum of averages
            ('total_amt_per_del', str(avg_amt_per_delivery())), #Avg Amt Per Delivery
            ('actual_target_delta_del', str(get_deliveries_delta())), #Actual Num Deliveries made over the Target
            ('total_savings', str(get_total_potential_savings())) #Total Potential Savings ($)
        ]
    )
    return data

def write_all_values_to_json():
    '''Write the data values to json-formatted text for easy access from js'''
    data = dict(
        [
            ('total_actual_del', str(get_total_actual_deliveries())), #Total tank deliveries with at least 1 delivery
            ('total_amt_del', str(get_total_actual_amt_delivered())), #Total Amt Delivered from sum of averages
            ('total_amt_per_del', str(avg_amt_per_delivery())), #Avg Amt Per Delivery
            ('actual_target_delta_del', str(get_deliveries_delta())), #Actual Num Deliveries made over the Target
            ('total_savings', str(get_total_potential_savings())) #Total Potential Savings ($)
        ]
    )

    try:
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    except:
        print("write error")

def print_export_tests():
    # Get Total Deliveries
    print("Total Actual Deliveries Made: " + str(get_total_actual_deliveries()))

    # Get Target Deliveries
    print("Total Target Deliveries: " + str(get_total_target_deliveries()))
    
    #Get Total Amt Delivered
    print("Total Amt Delivered from sum of averages: " + str(get_total_actual_amt_delivered()))

    #Get Avg Amt Per Delivery
    print("Avg Amt Per Delivery: " + str(avg_amt_per_delivery()))

    #Get the Deliveries Delta between Actual and Target
    print("Actual # Deliveries made over the Target: " + str(get_deliveries_delta()))

    #Get the Delivery Efficiency
    print("Total Delivery Efficiency: " + str(get_delivery_efficiency()) + "%")

    #Get the Total Estimated Potential Savings
    print("Total Potential Savings: $" + str(get_total_potential_savings()))

    #Get the Volume Amt Efficiency
    print("Volume Amt Efficiency: " + str(get_delivery_amt_efficiency()) + "%")

def print_report_tests():
    #Get count of total report rows (tanks)
    print("Total Tank Count: " + str(get_total_tank_count()))
    #Get count of active report rows (tanks)
    print("Active Tank Count: " + str(get_active_tank_count()))


# Run Tests
print_export_tests()

#print_report_tests()
