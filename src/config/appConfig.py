import pandas as pd


def getConfig(configFilename='config.xlsx') -> dict:
    """[summary]
    Get the application config from config.xlsx file
    Returns:
        dict: The application configuration as a dictionary
    """

    df = pd.read_excel(configFilename, header=None, index_col=0)
    configDict = df[1].to_dict()
    return configDict
