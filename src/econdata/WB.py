import pandas as pd
import requests
import itertools



def get_data(countries, indicators, fechaini, fechafin):
    
    ''' Importar múltiples series de la API del Banco Mundial.
    
    Parámetros
    ----------
    countries: dict
        Diccionario de los códigos y nombres de los países.
        >>>  countries = {'PE': 'Perú'}
    indicators: dict
        Diccionario de los códigos de los indicadores o series.
        Se obtienen de: 'https://datos.bancomundial.org/indicator/'
        >>> indicators = {'NY.GDP.PCAP.PP.KD': 'GDP per capita, PPP (US$ 2017)'}
    fechaini: str
        Fecha de inicio de la serie.
        >>> Anual: yyyy
    fechafin: str
        Fecha de fin de la serie.
        >>> Anual: yyyy
        
    Retorno
    ----------
    df: pd.DataFrame
        Países con las series consultadas.    
    
    Documentación
    ----------
    https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure

    '''


    df = pd.DataFrame()
        
    
    for c_k, c_n in countries.items(): 
        for i_k, i_n in indicators.items():
                
            url = f'http://api.worldbank.org/v2/country/{c_k}/indicator/{i_k}?format=json'
                 
            r = requests.get(url) 
            raise Exception('Vinculacion inválida!') if r.status_code != 200 else None            
            response = r.json()[1]
            
            values_list = []
            time_list   = []
                
            for j in response: 
                values_list.append(j['value'])
                time_list.append(j['date'])
                
            # Formats
            dictio = pd.DataFrame({'time': time_list, f'{i_k}': values_list})
            dictio.set_index('time', inplace = True)
            dictio.sort_index(ascending=True, inplace=True)
            dictio.rename(indicators, axis=1, inplace=True)
            
            # MultiIndex
            dictio.columns = pd.MultiIndex.from_tuples([(c_n, i_n)])
            
            # Merge
            df = pd.concat([df, dictio], axis=1)

    df = df.loc[fechaini: fechafin]
    
    return df




def search(consulta):
        
    ''' Extraer metadatos.
    
    Parámetros
    ----------
    consulta: list
        Dos palabras clave de la consulta.
        También se puede consultar en: https://datos.bancomundial.org/indicator/
        
    Retorno: 
    ---------
    df: pd.DataFrame
       Series consultadas.

    '''


    consulta = [w.lower() for w in consulta]
    
    # Combinations of words
    combs = list(itertools.permutations(consulta))
    combinations = []
    for co in combs:
        combination = '%20'.join(co)
        combinations.append(combination)
    
    # Query
    list_id    = []
    list_names = []
    
    for f in combinations:
        try:
            url = f'http://api.worldbank.org/v2/sources/2/search/{f}?format=json'
            r = requests.get(url) 
            response = r.json()['source'][0]['concept']    
        
            for res in response:
                try:
                    ii = res['variable']
                    for i in ii:
                        list_id.append(i['id'])
                        list_names.append(i['metatype'][0]['value'])
                except:
                    pass
        except:
            pass

    df = pd.DataFrame({'id': list_id, 'title': list_names})
    df.set_index('id', inplace=True)
    df = df.drop_duplicates() # Drop duplicated searchs
    df = df[~df.index.str.contains('~')]
    
    
    if df.empty is True:
        print('No encontrado!')
    else:
        return df