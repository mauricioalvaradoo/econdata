import pandas as pd
import requests



def get_data(series, fechaini, fechafin):

    ''' Importar multiples series de la API del BCRP.
    Considerar que las series deben ser de la misma frecuencia.
    
    Parámetros
    ----------
    series: dict
        Diccionario de los códigos y nombres de las series.
    fechaini: str
        Fecha de inicio de la serie.
    fechafin: str
        Fecha de fin de la serie.
        
    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas.
    
    Ejemplo
    ----------
    Formatos para fechas:
    >>> Diario: yyyy-mm-dd
    >>> Mensual: yyyy-mm
    >>> Trimestral: yyyyQq
    >>> Anual: yyyy
    
    Observación
    ----------
    1. A veces las consultas a series 'trimestrales' extraen entre 1-4
       trimestres más o menos de los solicitados. Para evitar estos problemas
       de consulta con el servidor, consultar las 'fechaini' y 'fechafin' de
       inicio (Q1) al fin (Q4) de un rango temporal. Ejemplos:
           - 2000Q1-2022Q4
           - 1980Q1-2019Q4
           - etc...


    Documentación
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api
    
    '''


    keys = list(series.keys())
    keysf = '-'.join(keys)    

    base = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api'

    url = f'{base}/{keysf}/json/{fechaini}/{fechafin}/ing'
    r = requests.get(url)
    
    try:
        response = r.json().get('periods')
    except ValueError:
        print('Error: Revisar que el formato de las fechas')
        print(' >>> Diario: yyyy-mm-dd\n >>> Mensual: yyyy-mm')
        print(' >>> Trimestral: yyyyQq\n >>> Anual: yyyy')
        return

    list_values = []
    list_time   = []

    for i in response:
        list_values.append(i['values'])    
        list_time.append(i['name'])

    df = pd.DataFrame(list_values)
    df = df.replace({'n.d.': None}) # Replace null values
    df = df.astype('float') # Set float format
    df.index  = list_time
    df.columns = list(series.values())


    # Formatos de fechas
    if keys[0][-1] == 'D':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%d.%b.%y')
    if keys[0][-1] == 'M':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%b.%Y')
    if keys[0][-1] == 'Q':
        try:
            df.index = df.index.map(lambda x: f"{x.split('.')[1]}{x.split('.')[0]}")
            new_fechaini = fechaini[0:2] + df.index[0]
            new_fechafin = fechafin[0:2] + df.index[-1]
            df.index = pd.period_range(new_fechaini, new_fechafin, freq='Q')
        except:
            pass
    if keys[0][-1] == 'A':
        df.index = pd.to_datetime(df.index, format='%Y').year
    
    df.sort_index(inplace=True) # Ordenamiento de fechas

    return df



def metadatos():

    metadatos = 'https://raw.githubusercontent.com/mauricioalvaradoo/'+\
                'econdata/master/src/econdata/metadata/BCRPData-metadata.csv'
    df = pd.read_csv(metadatos, index_col=0, sep=';', encoding='latin-1').reset_index()
    df = df[['Código de serie', 'Grupo de serie', 'Nombre de serie', 'Frecuencia', 'Fecha de inicio', 'Fecha de fin']]

    return df



def search(consulta, grupo=None, frecuencia=None):

    ''' Extraer código de la consulta.
    
    Parámetros
    ----------
    consulta: list
        Palabras claves de las series.
    grupo: list
        Palabras claves de los grupos. Default: None.
    frecuencia: str
        Frecuencia de la serie consultada. Default: None.
        >>> 'Diaria'
        >>> 'Mensual'
        >>> 'Trimestral'
        >>> 'Anual'

    Retorno
    ----------
    df: pd.DataFrame
        Metadatos de las series consultadas.
    
    Documentación
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/metadatos
    
    '''
    
    df = metadatos()
    consulta = [x.lower() for x in consulta]

    # Frecuencia
    if frecuencia is not None:
        try:
            df = df[df['Frecuencia'] == str(frecuencia)]
        except:
            pass
    
    # Grupo
    if grupo is not None:
        grupo = [x.lower() for x in grupo]
        
        for i in grupo:
            try:
                filter = df['Grupo de serie'].str.lower().str.contains(i)
                df = df[filter]
            except:
                pass

    # Series
    for i in consulta:           
        try:
            filter = df['Nombre de serie'].str.lower().str.contains(i)
            df = df[filter]
        except:
            df = print('Consulta no encontrada!')
    
    df.set_index('Código de serie', inplace=True)
    return df



def documentation(code):
    
    ''' Extraer microdatos del código de la serie.
    
    Parámetros
    ----------
    code: str
        Código base de la serie.

    Retorno
    ----------
    df: pd.DataFrame
        Metadatos de las series consultadas.
      
    Documentación
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/metadatos
    
    '''

    df = metadatos()
    df = df[df['Código de serie'] == str(code)]

    return df


