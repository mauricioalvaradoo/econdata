import pandas as pd
import requests 



def get_data(identifier, countries, serie, fechaini, fechafin, periodicidad):
    
    ''' Importar multiples series de la API de la OCDE.
    
    Parámetros
    ----------
    identifier: str
        Código identificador de la base de datos.
    countries: dict
        Códigos y nombres de los países (keys, values).
    serie: str
        Código de la serie.
    fechaini: str
        Fecha de inicio (yyyy-qq) .
    fechafin: str
        Fecha de fin (yyyy-qq).
    periodicidad: str
        Frecuencia de los datos: 'Q', 'Y'.  
    
    Retorno
    -------
    df: pd.DataFrame
        Series consultadas.
    
    Documentación
    -------
    https://stats.oecd.org/
    
    '''

    base = 'https://stats.oecd.org/SDMX-JSON'
    filters = '+'.join(countries.keys())
    nombres = list(countries.values())
    cantidad_paises = len(countries.keys())
    
    url = f'{base}/data/{identifier}/{filters}.{serie}/all?startTime={fechaini}&endTime={fechafin}'

    r = requests.get(url)
    if r.status_code == 200:
        pass
    else:
        print('Vinculacion inválida!')
    series = r.json()['dataSets'][0]['series']    
    
    df = pd.DataFrame()
    j = 0

    for i in range(0, cantidad_paises):
        fechas = list(list(series.values())[i]['observations'].keys())    # Índices con fechas
        valores = list(list(series.values())[i]['observations'].values()) # Valores en bruto
        
        # Extraer los valores limpios
        nv = []
        for i in range(0, len(fechas)):
            nv.append(valores[i][0])

        if df.empty == True:
            df = pd.DataFrame({'fechas': fechas, nombres[j]: nv})
        else:
            df2 = pd.DataFrame({'fechas': fechas, nombres[j]: nv})
            df = df.merge(df2, how='inner')
        j += 1    
      
    df = df.set_index('fechas')
    df.index = pd.period_range(fechaini, fechafin, freq=periodicidad)
    df.sort_index(inplace=True)
    df = df.astype('float')
    
    return df