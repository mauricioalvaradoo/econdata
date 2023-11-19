import pandas as pd
import requests



def get_data(cod_series: str, fechaini: str, fechafin: str) -> tuple[pd.DataFrame, str]:

    ''' Importar una serie de la API del BCRP.
    Considerar la frequencia de las serie para la fecha inicial y final.
    
    Parámetros
    ----------
    cod_series: str
        Código base de la serie.
    fechaini: str
        Fecha de inicio de la serie.
    fechafin: str
        Fecha de fin de la serie.
        
    Retorno
    ----------
    Tuple: pd.DataFrame, str
        pd.DataFrame: Serie consultada.
        str: Nombre de la serie consultada
    
    Ejemplo
    ----------
    Formatos para fechas:
    >>> Diario: yyyy-mm-dd
    >>> Mensual: yyyy-mm
    >>> Trimestral: yyyyQq
    >>> Anual: yyyy
    
    Consejos
    ----------
    1. De preferencia, para datos 'trimestrales' definir la importación desde
    Q1 del año de 'fechaini' hasta Q4 del de 'fechafin' para que el 'formato'
    de las fechas se asigne correctamente. No obstante, se está contemplando
    que la API posiblemente brinde la información hasta el Q4 de la 'fechafin'
    así que no se generará ningún error.
    >>> fechaini: 1994Q1 (primer trimestre)
    >>> fechafin: 2019Q4 (último trimestre)

    2. En algunos de los casos, cuando se busca importar datos de un año, pero
    esa serie está en variaciones anuales, la API puede que importe la serie un
    año después del 'fechaini' definido. Una sencilla solución es definir un año
    antes del que realmente se desea importar para conseguir la serie con el
    periodo correcto.

    Documentación
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api
    

    @author: Mauricio Alvarado. @last_editor: Augusto Huerta
    
    '''
    base = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api'
    url = f'{base}/{cod_series}/json/{fechaini}/{fechafin}/ing'

    r = requests.get(url)
    
    if r.status_code == 200:
        pass
    else:
        print("Vinculacion inválida!", r.status_code)
        return r.status_code

    response_dict = r.json() 
    name_series = response_dict.get('config',{}).get('series', {})[0].get('name')
    periods = response_dict.get('periods')

    df = pd.DataFrame(periods)
    # Extract the float numbers from the "values" column in the df_copy DataFrame
    df['values'] = df['values'].apply(lambda x: x[0])
    # Convert the "float_values" column in the df_copy DataFrame to the float data type
    df['values'] = df['values'].astype(float)
    # Renaming the column "name" into "date"
    df.rename({"name":"date"}, axis=1, inplace=True)
    # Setting the column "name" as an index
    df.index = df["date"]
    # Getting rid of that column
    df.drop("date",axis=1,inplace=True)
    print("DataFrame procesado. Retornando df y name_series")
    
    # Formatos de fechas
    if cod_series[-1] == 'D':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%d.%b.%y')
    if cod_series[-1] == 'M':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%b.%Y')
    if cod_series[-1] == 'Q':
        try:
            df.index = pd.period_range(fechaini, fechafin, freq='Q')
        except: 
            try: # Hasta fecha fin Q4
                df.index = pd.period_range(fechaini, fechafin[:4]+'Q4', freq='Q')
            except: # Aumentando un año para series en var. %
                try:
                    newanio = str( int(fechaini[:4])+1 )
                    df.index = pd.period_range(newanio+fechaini[4:], fechafin, freq='Q')
                except:  
                    try: # Aumentando un año para series en var. % y hasta fechafin Q4 
                        newanio = str( int(fechaini[:4])+1 )
                        df.index = pd.period_range(newanio+fechaini[4:], fechafin[:4]+'Q4', freq='Q')
                    except:
                        pass
    if cod_series[-1] == 'A':
        df.index = pd.to_datetime(df.index, format='%Y').year
    
    
    df.sort_index(inplace=True) # Ordenamiento de fechas

    return df, name_series



def metadatos():

    metadatos = 'https://raw.githubusercontent.com/mauricioalvaradoo/econdata/master/src/econdata/metadata/BCRPData-metadata.csv'
    df = pd.read_csv(metadatos, index_col=0, sep=";", encoding="latin-1").reset_index()
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
    
    
    @author: Mauricio Alvarado
    
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



def documentation(cod_series):
    
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
    
    
    @author: Mauricio Alvarado
    
    '''

    df = metadatos()
    df = df[df['Código de serie'] == str(cod_series)]

    return df


