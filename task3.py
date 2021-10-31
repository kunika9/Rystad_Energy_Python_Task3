#import useful libraries
import pandas as pd
from calendar import monthrange
import matplotlib.pyplot as plt
from matplotlib import rcParams
from datetime import datetime


#read excel file
def read_file():
	xls = pd.ExcelFile('Task_Excel.xlsx')
	df = pd.read_excel(xls, 'Input')
	return df

#subset dataframe
def subset_df(df):
	dataframe = df[['Refinery ID', 'Refinery', 'Company', 'Continent', 'Country',
       'Unit Group', 'Unit Category', 'Unit detail', 'Event type',
       'Event detail', 'Installed Capacity', 'Outage', 'Start', 'End']]
    return dataframe

# Main function that calculates the average outage per month
def calculate_avg_outage():
	df = read_file()
	df = subset_df(df)

	split_df = pd.DataFrame()

	for index, row in df.iterrows():
	    start_from = row['Start'].month
	    start_year = row['Start'].year
	    iterate_for = 12*(row['End'].year - row['Start'].year)
	    iterate_for += row['End'].month - row['Start'].month + 1
	    for i in range(iterate_for):
	        row['Month'] = start_from
	        row['year'] = start_year
	        row['Days in month'] = monthrange(start_year, start_from)[1]
	        if row['Start'].month == row['End'].month and row['Start'].year == row['End'].year:
	            row['Number of days'] = (row['End'] - row['Start']).days + 1
	        elif row['Start'].year == start_year and row['Start'].month == start_from:
	            row['Number of days'] = row['Days in month'] - row['Start'].day + 1
	        elif row['End'].year == start_year and row['End'].month == start_from:
	            row['Number of days'] = row['End'].day
	        else:
	            row['Number of days'] = row['Days in month']
	        row['Outage average per month'] = (row['Outage']*row['Number of days'])/row['Days in month']
	        split_df = split_df.append(row, ignore_index=True)
	        if start_from%12 == 0:
	            start_year+=1
	        start_from = (start_from%12)+1

	split_df['Number of days'] = split_df['Number of days'].astype(int)
	split_df['Month'] = split_df['Month'].astype(int)
	split_df['year'] = split_df['year'].astype(int)
	split_df['Days in month'] = split_df['Days in month'].astype(int)
	return split_df

# Output_graph is plotted using this function
def graph_using_groupby(df):
	rcParams['figure.figsize'] = 25, 8
	df['Date'] = df.apply(lambda x: datetime(x['year'], x['Month'], 1).date(), axis=1)
	new_df = df.groupby(['Date']).agg({
		"Outage average per month": "mean",
		"Installed Capacity" : "mean"
		})
	plt.plot(new_df['Outage average per month'], label=['Outage avg'])
	plt.plot(new_df['Installed Capacity'], label=['Installed Capacity'])
	plt.legend(loc=1)
	plt.grid(True)
	plt.show()
	#plt.savefig('Output_graph.png')


df = calculate_avg_outage()
print(df)
graph_using_groupby(df)

def normal_graph_without_using_groupby(df):
	rcParams['figure.figsize'] = 25, 8
	df['Date'] = df.apply(lambda x: datetime(x['year'], x['Month'], 1).date(), axis=1)
	df.plot(x='Date', y='Outage average per month', label='Outage avg with date graph')
	plt.grid(True)
	plt.show()
	df.plot(x='Date', y='Installed Capacity', label='Installed Capacity with date graph')
	plt.grid(True)
	plt.show()

# Graph as per individual refinery Id, it takes refinery_id and main df as parameters
def plot_as_per_refinery_id(refinery_id, df):
    df['Date'] = df.apply(lambda x: datetime(x['year'], x['Month'], 1).date(), axis=1)

    df = df[df['Refinery ID'] == refinery_id]
    
    plt.plot(df['Date'], df['Outage average per month'], label = 'Avg Outage')
    plt.plot(df['Date'], df['Installed Capacity'] , label = 'Installed Capacity')
    plt.legend(loc = 1)
    plt.grid(True)
    plt.show()

#plot_as_per_refinery_id('USA132', df)