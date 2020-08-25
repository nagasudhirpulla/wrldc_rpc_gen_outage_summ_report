'''
This script creates rpc forced, RSD, non RSD outage hours report
'''
# %%
import argparse
import datetime as dt
import pandas as pd
from src.config.appConfig import getConfig
from src.fetchers.outagesFetcher import fetchGenUnitOutagesForWindow

# get start and end dates from command line
startDate = dt.datetime(2020, 4, 1)
endDate = dt.datetime(2020, 4, 1)

# %%
# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()
# setup firstname, lastname arguments
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter last date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()
# access each command line input from the dictionary
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

# %%
endDate = endDate.replace(hour=23, minute=59, second=59)

print('startDate = {0}, endDate = {1}'.format(dt.datetime.strftime(
    startDate, '%Y-%m-%d'), dt.datetime.strftime(endDate, '%Y-%m-%d')))

# get application config
appConfig = getConfig()

reportsConStr = appConfig['reportsConStr']
outages = fetchGenUnitOutagesForWindow(reportsConStr, startDate, endDate)

outagesDf = pd.DataFrame(columns=outages['columns'], data=outages['rows'])
outagesDf['outHrs'] = ((outagesDf['REVIVED_DATETIME'] -
                        outagesDf['OUTAGE_DATETIME']).dt.total_seconds())*(1/3600)
# %%
# outagesDf.to_excel('dumps/data.xlsx')


# %%
capacitySeries = outagesDf.groupby('ELEMENT_NAME')[
    'CAPACITY'].agg(lambda x: x.iloc[0])
# %%
forcedOutagesDf = outagesDf[outagesDf['SHUTDOWN_TYPENAME'] == 'FORCED']
forcedOutagesSumm = forcedOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
    forcedHrs='sum', forcedOutagesCount='count')
# %%
plannedRsdOutagesDf = outagesDf[(outagesDf['SHUTDOWN_TYPENAME'] == 'PLANNED') & ((outagesDf['SHUTDOWN_TAG'] == 'RSD') | (
    outagesDf['SHUTDOWN_TAG'] == 'No Schedule') | (outagesDf['SHUTDOWN_TAG'] == 'Less Schedule'))]
plannedRsdOutagesSumm = plannedRsdOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
    rsdHrs='sum', rsdOutagesCount='count')

# %%
plannedNonRsdOutagesDf = outagesDf[(outagesDf['SHUTDOWN_TYPENAME'] == 'PLANNED') & (outagesDf['SHUTDOWN_TAG'] != 'RSD') & (
    outagesDf['SHUTDOWN_TAG'] != 'No Schedule') & (outagesDf['SHUTDOWN_TAG'] != 'Less Schedule')]
plannedNonRsdOutagesSumm = plannedNonRsdOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
    nonRsdHrs='sum', nonRsdOutagesCount='count')

# %%
reportDf = forcedOutagesSumm.merge(plannedRsdOutagesSumm, on='ELEMENT_NAME', how='outer').merge(
    plannedNonRsdOutagesSumm, on='ELEMENT_NAME', how='outer')
reportDf['CAPACITY'] = capacitySeries
nowTimeStr = str(dt.datetime.timestamp(dt.datetime.now())).replace('.', '')
reportDf.to_excel('dumps/report_data_{0}.xlsx'.format(nowTimeStr))

# %%
print('execution complete...')
