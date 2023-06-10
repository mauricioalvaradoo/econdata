import pandas as pd
import requests



def get_data(series, fechaini, fechafin):

    ''' Importar multiples series de la API del BCRP.
    Considerar que las series deben ser de la misma frecuencia.
    
    Parámetros
    ----------
    series: dict
        Diccionario de los códigos y nombres de las series.
    fechaini: datetime
        Fecha de inicio de la serie.
    fechafin: datetime
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
    

    @author: Mauricio Alvarado
    
    '''

    keys = list(series.keys())
    
    
    df = pd.DataFrame()
    base = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api'
        

    for i in keys:
        url = f'{base}/{i}/json/{fechaini}/{fechafin}/ing'

        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print('Vinculacion inválida!')
            break
        
        response = r.json().get('periods')
        
        list_values = []
        list_time = []
                
        for j in response:
            list_values.append(float(j['values'][0]))    
            list_time.append(j['name'])

        # Merge
        dic = pd.DataFrame({'time': list_time, f'{i}': list_values})                      
        df = pd.concat([df, dic]) if df.empty is True else pd.merge(df, dic, how='outer')
        
    df.set_index('time', inplace=True)
    df.rename(series, axis=1, inplace=True)


    # Formatos de fechas
    if keys[0][-1] == 'D':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%d.%b.%y')
    if keys[0][-1] == 'M':
        df.index = df.index.str.replace('Set', 'Sep')
        df.index = pd.to_datetime(df.index, format='%b.%Y')
    if keys[0][-1] == 'Q':
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

    return df



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
    
    
    @author: Mauricio Alvarado
    
    '''

    df = metadatos()
    df = df[df['Código de serie'] == str(code)]

    return df


