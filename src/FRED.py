import pandas as pd
import numpy as np
import requests 



def get_data(series, api_key, fechaini, fechafin):
    
    """ Importar múltiples series de la API del FRED
    
    Parámetros
    ----------
    series: dict
        Diccionario de los códigos y nombres de las series
    api_key: str
        API Key del desarrollador: https://fred.stlouisfed.org/docs/api/api_key.html
    fechaini: str
        Fecha de inicio de la serie  
    fechfin: str
        Fecha de fin de la serie
 
    Retorno 
    ----------
    df: pd.DataFrame
       Series consultadas
    
    Ejemplo
    ----------
    Formatos para fechas:
    >>> Diario: yyyy-mm-dd
    >>> Mensual: yyyy-mm
    >>> Anual: yyyy   
        
    Documentación
    ----------
    https://fred.stlouisfed.org/docs/api/fred/
    

    @authors: Norbert Andrei Romero Escobedo, Mauricio Alvarado
    
    """
    
    
    keys = list(series.keys())

    df = pd.DataFrame()
    
    for i in keys:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={i}&api_key={api_key}&file_type=json"
    
        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print("Porfavor, revisa los datos ingresados.")
            break
    
        observations = r.json().get("observations")
    
        list_values = []
        list_time = []
        
        for j in observations:
            list_values.append(j["value"])
            list_time.append(j["date"])


        dictio = pd.DataFrame({"time": list_time, f"{i}": list_values})
        df = dictio if df.empty is True else pd.merge(df, dictio, how = "outer")

    df.set_index("time", inplace=True)
    df.rename (series, axis = 1, inplace = True)
    df = df.loc[fechaini: fechafin]
    
    # Corrigiendo '.' for missing values   
    for i in df.columns:
        try:
            df.loc[df[i] == '.', i] = np.nan
            df[i] = df[i].astype('float')
        except:
            pass
    
    return df




def search(consulta, api_key):
    
    """ Extraer metadatos de las consultas

    Parámetros
    ----------
    consulta: list
        Palabras claves de las consultas  
    api_key: str
        API Key del desarrollador: https://fred.stlouisfed.org/docs/api/api_key.html
    
    Retorno
    ----------
    df: pd.DataFrame
       Series consultadas
    

    @authors: Norbert Andrei Romero Escobedo, Mauricio Alvarado
    
    """
    
    formato = "+".join(consulta)
    formato = formato.lower()

    url = f"https://api.stlouisfed.org/fred/series/search?search_text={formato}&api_key={api_key}&file_type=json"
    r = requests.get(url) 

    response = r.json()["seriess"]

    list_id = []
    list_title = []
    list_start = []
    list_end = []
    list_frequency = []
    list_seasonal_adjusment = []

    for i in response:
        list_id.append(i['id'])
        list_title.append(i['title'])
        list_start.append(i['observation_start'])
        list_end.append(i['observation_end'])
        list_frequency.append(i['frequency'])
        list_seasonal_adjusment.append(i['seasonal_adjustment'])

    df = pd.DataFrame({
        "id": list_id,
        "title": list_title,
        "start": list_start,
        "end": list_end,
        "frequency": list_frequency,
        "seasonal_adjusment": list_seasonal_adjusment
    })

    df.set_index("id", inplace=True) 

    return df

