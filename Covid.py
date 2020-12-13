import logging

def import_data():
    '''
    Function to import monthlt operations data

    Outputs
    |   df: DataFrame: Monthly Operations Data
    '''
    import pandas as pd
    logging.info('Getting Monthly Operations Data')
    file= 'Covid_Data.csv'
    df = pd.read_csv(file, thousands=',') # import data with "," as a thousands seperator
    #Feature Engineer Totals for Air Taxi, Commercial, GA, Military
    df['Total Air Carrier'] = df['IFR Air Carrier'] + df['VFR Air Carrier']
    df['Total Air Taxi'] = df['IFR Air Taxi'] + df['VFR Air Taxi']
    df['Total GA'] = df['IFR GA'] + df['VFR GA'] + df['Local Civil']
    df['Total Military'] = df['IFR Military'] + df['VFR Military'] + df['Local Military'] 
    df['Date'] = pd.to_datetime(df['Date'], format="%b-%y")
    return df

def ops_percentages(df):
    '''
    Utility fucntion to find Percentage of GA and Commercial Operations

    Inputs
    |   df: DataFrame: Operations Data

    Outputs
    |   df: DataFrame: Facilty name, Total ops, Percentage Data
    '''
    #Subset Latest full year of Data
    df = df[df['Calendar Year']==2019]
    #Add all operations
    df['Total'] = df['Total Air Carrier'] + df['Total Air Taxi'] + df['Total GA'] + df['Total Military']
    #Find Percentages
    df['2019 Percent GA'] = df['Total GA'] / df['Total'] * 100
    df['2019 Percent Air Carrier'] = df['Total Air Carrier'] / df['Total'] * 100
    logging.debug('Percentages found')
    return df[['Facility', 'Total', '2019 Percent GA', '2019 Percent Air Carrier']]

def section_airports(x):
    '''
    Utility function to bi airports by operations

    Inputs
    |   df: DataFrame: Percent operations Data

    Outputs
    |   y: Int: Bin number for desired airport
    |   |   1: Almost all GA operations
    |   |   2: Mostly GA operations
    |   |   3: Split operations
    |   |   4: Mostly commercial operations
    |   |   5: Almost all commercial operations
    '''
    if x['2019 Percent GA'] >= 80:
        y = 1
    elif x['2019 Percent GA'] >= 60:
        y = 2
    elif x['2019 Percent GA'] >= 40:
        y = 3
    elif x['2019 Percent GA'] >= 20:
        y = 4
    else:
        y = 5
    return y

def plot_monthly_trends(df):
    '''
    Plots monthly operations data for each airport section
    '''
    import matplotlib.pyplot as plt
    #Iterate through all airport section and plot
    for x in range(1,6):
        a= df.loc[x]
        plt.plot(a.index, a['Total'])
    plt.xlabel('Date')
    plt.ylabel('Operations')
    plt.legend(['GA Airports','Mostly GA Airports', 'About 50/50 Airports', 'Mostly Commerical Airports', 'Commercial Airports'])
    plt.title('Airport Operations from Oct-19 to Oct-20')
    plt.grid(True)
    plt.show()
    logging.debug('Regular ops graph success')

def plot_percentages(df):
    '''
    Plots monthly operations data in percentages for each airport section
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    #Iterate through all airport section and plot
    for x in range(1,6):
       a=df.loc[x]
       a = a[a.index=='2019-10-01']['Total'].item()
       b=df.loc[x]['Total'].to_numpy()
       plt.plot(df.loc[x].index, b/a * 100)
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel("% of Operations")
    plt.title("Percentage of Operations Compared to Oct '19")
    plt.legend(['GA Airports','Mostly GA Airports', 'About 50/50 Airports', 'Mostly Commerical Airports', 'Commercial Airports'])
    plt.show()
    logging.debug('Percentage ops graph success')