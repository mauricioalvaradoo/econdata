import pandas as pd
import requests 



def get_data(countries, indicator, fechaini, fechafin):
    
    """ Importar múltiples series de la API del Banco Mundial
    
    Parámetros
    ----------
    countries: dict
        Diccionario de los códigos y nombres de los países
        >>>  countries = {"PE": "Perú"}   
    indicator: str
        Código del indicador o serie
        Se obtiene de: "https://datos.bancomundial.org/indicator/"        
    fechaini: str
        Fecha de inicio de la serie
        >>> Anual: yyyy
    fechafin: str
        Fecha de fin de la serie
        >>> Anual: yyyy
        
    Retorno
    ----------
    df: pd.DataFrame
        Países con las series consultadas.    
    
    Documentación
    ----------
    https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure
    
    
    @authors: Mauricio Alvarado, Norbert Andrei Romero Escobedo

    """


    keys = list(countries.keys())
    df = pd.DataFrame()
    

    for i in keys:
        url = f"http://api.worldbank.org/v2/country/{i}/indicator/{indicator}?format=json"
         
        r = requests.get(url) 
                
        if r.status_code == 200:
            pass
        else:
            print("Revisa los datos ingresados")
            break
    
        response = r.json()[1]
    
        values_list = []
        time_list = []
    
        for j in response: 
            values_list.append(j["value"])
            time_list.append(j["date"])
        
        # Merge
        dictio = pd.DataFrame({"time": time_list, f"{i}": values_list})
        df = pd.concat([df, dictio]) if df.empty is True else pd.merge(df, dictio, how = "outer")
    
    df.set_index("time", inplace = True)
    df.sort_index(ascending=True, inplace=True)
    df.rename(countries, axis=1, inplace=True)

    df = df.loc[fechaini: fechafin]
    
    return df
      
          
      
      
def search(consulta):
        
    """ Extraer metadatos
    
    Parámetros
    ----------
    consulta: list
        Dos palabras clave de la consulta
        
    Retorno: 
    ---------
    df: pd.DataFrame
       Series consultadas
    
    @authors: Mauricio Alvarado, Norbert Andrei Romero Escobedo  

    """


    formato = "%20".join(consulta)
    formato = formato.lower()
   
    url = f"http://api.worldbank.org/v2/sources/2/search/{formato}?format=json"
    r = requests.get(url) 
    response = r.json()["source"][0]["concept"][1]["variable"]
    

    list_id= []
    list_names= []
    
    for i in response: 
        list_id.append(i["id"])
        list_names.append(i["name"])
        
    df= pd.DataFrame({ "id": list_id, "title": list_names})

    return df