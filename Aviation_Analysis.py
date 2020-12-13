#Imports needed for multiple functions
import pandas as pd
import logging

def main():
    '''
    Main function that is ran when module is called from the command line.
    For help on input commands please type "Analysis_Aviation.py -h" from the command line
    Outputs desired data and a necessary analysis plots
    '''
    import argparse, Covid
    #Initiate logger
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # Add debug file capabilities
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s')
    d_file = logging.FileHandler('Aviation_Analysis.log','w')
    d_file.setLevel(logging.DEBUG)
    d_file.setFormatter(formatter)
    log.addHandler(d_file)
    # Add sys.stdout info message capabilities
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    log.addHandler(stream)
    #Import Data
    data = import_ops_data()
    airport = import_airport_info() 
    # Below lines define arguments for command line
    parser = argparse.ArgumentParser(description='Analysis of Airport Data')
    # Airport Trends or COVID Analysis
    parser.add_argument('analysis', metavar='<anaylsis>', choices=['trends', 'covid'], help='Type of Analysis')
    # Choose to look at a airport, state, or region
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a','--airport', metavar='<airport>', choices=airport.Abbr.unique(), dest='airport', help='3 letter FAA abbreviation of an airport')
    group.add_argument('-s','--state', metavar='<state>', choices=airport.State.unique(), dest='state',help='2 letter state abbreviation')
    group.add_argument('-r','--region', metavar='<region>', choices=airport.Region.unique(), dest='region', help='3 letter FAA abbreviation of a region')
    #Output file designation
    parser.add_argument('-o', '--ofile', metavar='<outfile>', dest='ofile', help='File to write to. If not specified, it writes to sys.stdout')
    args= parser.parse_args()
    logging.debug('Inputs Given: Command : {} , Facility : {}, State : {}, Region : {}, O-File : {}'.format(args.analysis, args.airport, args.state, args.region, args.ofile))
    #Combine dataframes
    data=pd.merge(data, airport, left_on='Facility', right_on='Abbr')
    if args.analysis == 'trends':
        if args.airport != None:
            #Analysis trends for desired airport
            df = data_option(data, args.airport, 'Facility')
            plot_trends_data(df, args.airport, 'Airport')
        elif args.state != None:
            #Analysis trends for desired state
            df = data_option(data, args.state, 'State')
            plot_trends_data(df, args.state, 'State')
        elif args.region != None:
            #Analysis trends for desired aregion
            df = data_option(data, args.region, 'Region')
            plot_trends_data(df, args.region, 'Region')
        write_output_file(args.ofile, df)   #Write DF to file
    elif args.analysis == 'covid':
    #Simple Covid Analysis, Most work done in Covid.py
        df = Covid.import_data()
        ops = Covid.ops_percentages(data[data['Calendar Year']==2019])
        df=pd.merge(df, ops, on='Facility')
        df['Section'] = df.apply(Covid.section_airports, axis=1)
        logging.debug('Sectioning Complete')
        df = df.groupby(['Section','Date']).sum()
        df['Total'] = df['Total GA'] + df ['Total Air Carrier']  #Recalculate new Totals
        #Regualar anfd Percentage graphs
        logging.info('Graphing COVID Data')
        Covid.plot_monthly_trends(df)
        Covid.plot_percentages(df)

def plot_trends_data(df, opt, flag):
    '''
    Creates the output plots

    Inputs
    |   df: Dataframe: Data to plot
    |   opt: str: User given analysis option
    |   flag: str: Type of opt
    '''
    logging.info('Creating Plot')
    import matplotlib.pyplot as plt

    plt.plot(df.loc[:'2019'])
    plt.grid(True)
    plt.legend(df.columns)
    plt.ylabel('# of Operations')
    plt.xlabel('Year')
    if flag != 'State':
        plt.title('Aviation Trends of {} {}'.format(opt,flag))
    else:
        plt.title('Aviation Trends of {}'.format(opt))
    plt.show()
    logging.debug('Succesfully created plot for {} {}'.format(opt, flag))

def write_output_file(file_opt, df):
    '''
    Utility function to write data to specified file

    Inputs
    |   file_opt: str: file to write to. Write stdout if not provided
    |   df: DataFrame: Data to write
    '''
    
    if file_opt == None:
        #Write to stdout if no file given
        logging.info('Writing to sys.stdout')
        print(df)
    else:
        # Write to given file
        logging.info('Writing to {}'.format(file_opt))
        df.to_csv(file_opt)
    logging.debug('Succesfully wrote to file')

def data_option(df, opt, flag):
    '''
    Utility function to get filtered data for trends

    Inputs
    |   df: Pandas Dataframe: Dataframe containing all of the data
    |   opt: Argument provided by user for analysis
    |   flag: str: Type of opt provided by user
    |   |   'Facility' - when argument flag is given
    |   |   'State' - when state argument is given
    |   |   'Region' - when region argument is given

    Output
    |   df: Pandas DataFrame: Filtered Data of elected analysis
    '''
    logging.info('Getting data for {}'.format(opt))
    df = df[df[flag] == opt]
    df = df.groupby(['Calendar Year']).sum()
    keep= ['Total Air Carrier', 'Total Air Taxi', 'Total GA', 'Total Military']
    return df[keep]

def import_ops_data(): 
    
    '''
    Import and clean operations data. Data is on a CSV file called Yearly_Data.csv
    Data is cleaned by droping irrelevant rows and adding Air Taxi, Commerical, GA, and Military columns.

    Output
    |   data: Pandas df - Cleaned Operationsa dataframe
    '''
    import logging
    logging.info('Getting Airport Operations Data')
    file= 'Yearly_Data.csv'
    data = pd.read_csv(file, thousands=',') # import data with "," as a thousands seperator
    # Drop "Overflight" operations
    columns_to_drop=['IFR Overflight Air Carrier', 'IFR Overflight Air Taxi', 'IFR Overflight GA', 
    'IFR Overflight Military', 'VFR Overflight Air Carrier', 'VFR Overflight Air Taxi', 'VFR Overflight GA', 
    'VFR Overflight Military', 'Unnamed: 20']
    data.drop(columns=columns_to_drop, inplace=True)
    #Feature Engineer Totals for Air Taxi, Commercial, GA, Military
    data['Total Air Carrier'] = data['IFR Itinerant Air Carrier'] + data['VFR Itinerant Air Carrier']
    data['Total Air Taxi'] = data['IFR Itinerant Air Taxi'] + data['VFR Itinerant Air Taxi']
    data['Total GA'] = data['IFR Itinerant GA'] + data['VFR Itinerant GA'] + data['Local Civil']
    data['Total Military'] = data['IFR Itinerant Military'] + data['VFR Itinerant Military'] + data['Local Military'] 
    logging.debug('Airport Operations Import Succesful')
    return data

def import_airport_info():
    '''
    Import and clean airport information. Information in held in a CSV file 'Airport_Info.csv'.
    Clean data sperates airport name and abbreviation as well as provides abbreviations for airport region

    Output
    |   data: Pandas Dataframe - Clean Airport information Dataframe
    '''
    logging.info('Getting Airport Information')
    #Import data
    file= 'Airport_Info.csv'
    data = pd.read_csv(file)
    # Save Facility column in array
    airports=data.Facility
    acc=[]
    name=[]
    #Seperate name and abbreviation in Facility column and save in list
    for airport in airports:
        acc.append(airport.split(':')[0])
        name.append(airport.split(':')[1])
    #Add name and Abbreviation list to datafrane
    data['Name']=name
    data['Abbr']=acc
    #Drop facility
    data.drop(columns='Facility', inplace=True)
    #Map given region digit to three letter abbreviation
    regions = {'5':'AAL', '3':'ACE', '1':'AEA', 'C':'AGL', 'E':'ANE', 'S':'ANM', '7':'ASO', '2':'ASW', '4':'AWP'}
    data['Region'] = data.Region.map(regions)
    logging.debug('Airport Info Import Succesful')
    return data  

if __name__=='__main__':
    # Run main program when called from command line
    main()