import pandas as pd
from pandas import DataFrame

def column_preci_treatment(file_route:str) -> DataFrame:
    r'''Function to preprocess column info from precipitation data from 
        Direccion Nacional de Meterología de Uruguay

        Receives
        --------
        file_route : str
            string that represents the file route to load the data from .csv

        Returns
        -------
        df : DataFrame
            DataFrame of processed columns
    '''
    
    # Data import
    df = pd.read_csv(# File route of csv
                     file_route,
                     # csv separator
                     sep = ';')

    if any(df.columns == 'Nombre'):

        # 'Nombre' field is dropped
        df = df.drop(columns=['Nombre'])

        # DataFrame transpose
        df = df.T

        # Index reboot
        df = df.reset_index()

        # Column names declaration
        df.columns = df.iloc[0]

        # Repeated row dropping
        df.drop(labels=0, axis=0, inplace=True)

    else:
        pass

    return df


def data_preci_treatment(file_route) -> DataFrame:
    r'''Function to preprocess precipitation data from Direccion Nacional de 
        Meterología de Uruguay

        Receives
        --------
        file_route : str
            string that represents the file route to load the data from .csv

        Returns
        -------
        df : DataFrame
            DataFrame of preprocessed data
    '''

    # Data import
    df = pd.read_csv(# Data route
                     file_route,
                     # NaN values masking
                     na_values=['s/dato'],
                     # csv separator
                     sep = ';')

    if any(df.columns == 'MES') and any(df.columns == 'AÑO'):

        # From month abbreviation to month number
        month_names = df['MES'].unique().tolist()
        month_dict = {v:f'{k:02d}' for k,v in enumerate(month_names, start=1)}
        df['MES'] = df['MES'].map(month_dict)

        # 'Fecha' column declaration
        df['Fecha'] = df['AÑO'].astype(str) +  '-' + df['MES']

        # 'AÑO' and 'MES' columns dropping
        df.drop(columns=['AÑO', 'MES'], inplace=True)

        # 'Fecha' placement at first column
        first_col = df.pop('Fecha')
  
        # First column insertion
        df.insert(0, 'Fecha', first_col)

        # DataFrame reshape
        df = pd.melt(# DataFrame to reshape
                     df, 
                    # Identifier variable
                    id_vars = ['Fecha'], 
                    # New column asignment
                    var_name=['Nombre Estación'], 
                    # New values to place in the dataframe
                    value_name= 'Precipitacion')

        # 'Fecha' colum  conversion from string to datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'])

    else:
        pass

    return df

def null_report(df:DataFrame) -> DataFrame:
    r'''
    Function to generate a null value report

    Receives
    --------

    df : DataFrame
        A dataframe to compute the null values

    Returns
    -------

    df_null_rep : DataFrame
        A dataframe that returns the null values per variable from the input df
    '''

    null_percentage = []
    column_names = df.columns

    for column in column_names:
        null_percentage += [df[column].isnull().sum()/len(df) * 100]

    # Dataframe null values percentage
    df_null_rep = pd.DataFrame({'variables':column_names,
                                'null_values': null_percentage})

    return df