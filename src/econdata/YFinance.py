import pandas as pd
import yfinance as yf



def get_data(series, tipo='Close', fechaini=None, fechafin=None):

    ''' Importar multiples series de la API de Yahoo Finance.
    
    Parámetros
    ----------
    series: dict
        Lista de los codigos de las series y nombres.
    tipo: str
        Serie consultada.
        >>> Close: Default
        >>> Open
        >>> High
        >>> Low
        >>> AdjClose
        >>> Volume
    fechaini: datetime
        Fecha de inicio de la serie.
    fechafin: datetime
        Fecha de fin de la serie.

    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas.
    
    Documentación
    ----------
    https://pypi.org/project/yfinance/
    
    '''
    
    
    keys = list(series.keys())
    df = pd.DataFrame()
    
    for key in keys:
        data = yf.Ticker(key)
        
        if (fechaini == None) or (fechafin == None):
            data = data.history(period='max')
        else:
            data = data.history(start=fechaini, end=fechafin)
        
        data.reset_index(inplace=True)
        data[key] = data[tipo]

        try: 
            # Quitar zona horaria
            data['Date'] = data['Date'].dt.tz_localize(None)
        except:
            pass
    
        # Merge
        df = pd.concat([df, data[['Date', key]]]) if df.empty is True else pd.merge(df, data[['Date', key]], how='outer')

    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df.sort_index(inplace=True)
    df = df.astype('float')
    df = df.rename(series, axis = 1)


    return df



def search(consulta):
    
    ''' Extraer código de la consulta.
    
    Parámetros
    ----------
    consulta: list
        Palabras claves de las series.

    Retorno
    ----------
    df: pd.DataFrame
        Metadatos de las series consultadas.
    
    Documentación
    ----------
    https://www.nasdaq.com/market-activity/stocks/screener
    
    '''
    
    df = pd.read_csv(
        'https://raw.githubusercontent.com/mauricioalvaradoo/econdata/master/src/econdata/metadata/Yahoo-Tickers.csv',
        index_col=0
    ).reset_index()
    df = df[['Symbol', 'Name', 'Country', 'IPO Year', 'Sector', 'Industry']]
    df.set_index('Symbol', inplace=True)
    
    consulta = [x.lower() for x in consulta]
    
    for i in consulta:           
        try:
            filter = df['Name'].str.lower().str.contains(i)
            df = df[filter]
        except:
            df = print('Consulta no encontrada!')
            return
        
    try:
        df['IPO Year'] = df['IPO Year'].astype('Int64')
    except:
        pass
    
    return df



