import pandas as pd
import requests



def get_data(indicator, countries=None, fechaini=None, fechafin=None):
    
    ''' Importar series de la API del FMI.
    
    Parámetros
    ----------
    indicator: str
        Código del indicador o serie.
        Se obtiene de: 'https://www.imf.org/external/datamapper/api/v1/'       
    countries: dict
        Diccionario de los códigos y nombres de los países. Default: None.
        >>> countries = {'PER': 'Perú'}   
    fechaini: str
        Fecha de inicio de la serie. Default: None.
        >>> Anual: yyy
    fechafin: str
        Fecha de fin de la serie. Default: None
        >>> Anual: yyyy
        
    Retorno
    ----------
    df: pd.DataFrame
        Países con las series consultadas.    
    
    Documentación
    ----------
    https://www.imf.org/external/datamapper/api/help
    
    
    @authors: Mauricio Alvarado

    '''
    
    base = 'https://www.imf.org/external/datamapper/api/v1/'
    
    # Filtros
    filters = '/'.join(countries.keys()) if countries is not None else None
    dates = [str(y) for y in range(int(fechaini), int(fechafin)+1)] if fechaini is not None and fechafin is not None else None
    dates = [str(y) for y in range(int(fechaini), 2029)]            if fechaini is not None and fechafin is     None else dates
    dates = [str(y) for y in range(1980, int(fechafin)+1)]          if fechaini is     None and fechafin is not None else dates
    dates = ','.join(dates) if dates is not None else None
    
    url = f'{base}{indicator}'
    
    if filters:
        url += f'/{filters}'      
    if dates:
        url += f'?periods={dates}'
    
    try:
        serie = requests.get(url).json()['values'][indicator]
        df = pd.DataFrame(serie)
        df.sort_index(inplace=True)
    except KeyError:
        return print(
            'El código de la serie o del país es incorrecto.',
            'En el caso del país, confirmar si está incluido en la base de datos del que pertenece la serie.')
        
    return df



def search(tipo, consulta=None):
    
    ''' Extraer código de la consulta.
    
    Parámetros
    ----------
    tipo: str
        Tipo de datos a consultar: 'Indicadores', 'Países', 'Regiones', 'Grupos'.
    consulta: list
        Palabras claves de consulta. Default: None.

    Retorno
    ----------
    df: pd.DataFrame
        Consulta.

    Documentación
    ----------
    * https://www.imf.org/en/Data
    * https://www.imf.org/external/datamapper/api/help


    @author: Mauricio Alvarado
    
    '''
    
    def search_df1(r):
        codes = []; names = []; units = []; datasets = []
        for i in list(r.keys()):
            codes.append(i)
        for i in list(r.values()):
            names.append(i['label'])
            units.append(i['unit'])
            datasets.append(i['dataset'])
        df1 = pd.DataFrame({'Código':codes,'Nombres':names,'Unidades':units,'Dataset':datasets})
    
        return df1
    
    def search_df2(r):
        codes = []; names = []
        for i in list(r.keys()):
            codes.append(i)
        for i in list(r.values()):
            names.append(i['label'])
        df2 = pd.DataFrame({'Código': codes, 'Nombres': names})
    
        return df2
    
    
    types = {
        'Indicadores': 'indicators',
        'Países': 'countries',
        'Regiones': 'regions',
        'Grupos': 'groups'
    }
    
    
    try:
        selection = types[tipo]
        url = f'https://www.imf.org/external/datamapper/api/v1/{selection}'
        r = requests.get(url).json()[selection]
        
        try: 
            df = search_df1(r)
        except:
            df = search_df2(r)
        
        df.dropna(inplace=True)

        if consulta is not None:
            consulta = [x.lower() for x in consulta]
                
            for i in consulta:
                filter = df['Nombres'].str.lower().str.contains(i)
                df = df[filter]

        else:
            pass
    
        df.set_index('Código', inplace=True)
    
        return df     
        
    except:
        return print('Revisa bien el tipo!')