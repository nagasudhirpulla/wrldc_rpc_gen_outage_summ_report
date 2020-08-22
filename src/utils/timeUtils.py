import datetime as dt
import pandas as pd


def getTimeDeltaFromDbStr(timeStr: str) -> dt.timedelta:
    """Convert db time string in reporting software to time delta object

    Args:
        timeStr (str): The string that represents time, like 14:25 or 15:23:45

    Returns:
        dt.timedelta: time delta that has hours and minutes components
    """
    if pd.isnull(timeStr):
        return dt.timedelta(seconds=0)
    elif not(':' in timeStr):
        return dt.timedelta(seconds=0)
    else:
        timeSegs = timeStr.split(':')
        timeSegs = timeSegs[0:2]
        return dt.timedelta(hours=int(timeSegs[0]), minutes=int(timeSegs[1]))
