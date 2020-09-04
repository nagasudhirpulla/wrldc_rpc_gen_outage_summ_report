from src.fetchers.outagesFetcher import fetchGenUnitOutagesForWindow
import pandas as pd
import datetime as dt


class RpcGenOutageHrsGenerator():
    def __init__(self, reportsConStr):
        self.reportsConStr = reportsConStr

    def getGenOutageHrs(self, startDate: dt.datetime, endDate: dt.datetime) -> pd.DataFrame:
        outages = fetchGenUnitOutagesForWindow(
            self.reportsConStr, startDate, endDate)

        outagesDf = pd.DataFrame(
            columns=outages['columns'], data=outages['rows'])
        outagesDf['outHrs'] = ((outagesDf['REVIVED_DATETIME'] -
                                outagesDf['OUTAGE_DATETIME']).dt.total_seconds())*(1/3600)
        outagesDf = pd.DataFrame(
            columns=outages['columns'], data=outages['rows'])
        outagesDf['outHrs'] = ((outagesDf['REVIVED_DATETIME'] -
                                outagesDf['OUTAGE_DATETIME']).dt.total_seconds())*(1/3600)

        capacitySeries = outagesDf.groupby('ELEMENT_NAME')[
            'CAPACITY'].agg(lambda x: x.iloc[0])

        forcedOutagesDf = outagesDf[outagesDf['SHUTDOWN_TYPENAME'] == 'FORCED']
        forcedOutagesSumm = forcedOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
            forcedHrs='sum', forcedOutagesCount='count')

        plannedRsdOutagesDf = outagesDf[(outagesDf['SHUTDOWN_TYPENAME'] == 'PLANNED') & ((outagesDf['SHUTDOWN_TAG'] == 'RSD') | (
            outagesDf['SHUTDOWN_TAG'] == 'No Schedule') | (outagesDf['SHUTDOWN_TAG'] == 'Less Schedule'))]
        plannedRsdOutagesSumm = plannedRsdOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
            rsdHrs='sum', rsdOutagesCount='count')

        plannedNonRsdOutagesDf = outagesDf[(outagesDf['SHUTDOWN_TYPENAME'] == 'PLANNED') & (outagesDf['SHUTDOWN_TAG'] != 'RSD') & (
            outagesDf['SHUTDOWN_TAG'] != 'No Schedule') & (outagesDf['SHUTDOWN_TAG'] != 'Less Schedule')]
        plannedNonRsdOutagesSumm = plannedNonRsdOutagesDf.groupby('ELEMENT_NAME')['outHrs'].agg(
            nonRsdHrs='sum', nonRsdOutagesCount='count')

        reportDf = forcedOutagesSumm.merge(plannedRsdOutagesSumm, on='ELEMENT_NAME', how='outer').merge(
            plannedNonRsdOutagesSumm, on='ELEMENT_NAME', how='outer')
        reportDf['CAPACITY'] = capacitySeries

        return reportDf
