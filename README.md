# Econdata
**Econdata** es una librería para la extracción de series de tiempo de las principales instituciones económicas para el Perú. En la versión actual se cuenta con las siguientes instituciones:
1. Banco Central de Reserva del Perú (BCRP)
2. Banco Mundial (WB) 
3. Federal Reserve Economic Data (FRED)
4. Fondo Monetario Internacional (IMF)
5. Organización para la Cooperación y el Desarrollo Económicos (OECD)
6. Yahoo! Finance (YFinance)


El anuncio fue realizado en LinkedIn, y está disponible [aquí](https://www.linkedin.com/posts/mauricioalvaradoo_github-mauricioalvaradooecondata-extracci%C3%B3n-activity-7053798889950179328-wl5w?utm_source=share&utm_medium=member_desktop). 


## Instalación
Para instalar la versión más reciente de econdata desde [PyPI](https://pypi.org/project/econdata/):
```python
pip install econdata
```

La librería requiere de las siguientes dependencias:
* pandas
* numpy
* yfinance
* requests
* warn


## Métodos
Para cada institución se tiene dos métodos comunes. El primero sirve para extraer las series dado un rango de peridos:
```text
get_data()
```

La segunda sirve para conseguir la metadata:
```text
search()
```
El resultado incluye los nombres, códigos y fechas que servirán como complemento con la función anterior: `get_data()`.


## Getting started
### Ejemplo: Extracción de datos del BCRP
Iniciaremos con la consulta del _PBI real en variaciones anuales_:

```python
from econdata import BCRP

BCRP.search(
    consulta=['PBI'],
    grupo=['Producto', 'variaciones'],
    frecuencia='Trimestral'
)
```

```text
                                                    Grupo de serie  \
Código de serie                                                      
PN02507AQ        Producto bruto interno (variaciones porcentuales)   
PN02526AQ        Producto bruto interno por tipo de gasto (vari...   

                Nombre de serie  Frecuencia Fecha de inicio Fecha de fin  
Código de serie                                                           
PN02507AQ            PBI Global  Trimestral         T1-1980      T4-2022  
PN02526AQ                   PBI  Trimestral         T1-1980      T4-2022
```

Tras obtener el código de la serie (```PN02526AQ```), se puede solicitar la data para un rango de periodos:

```python
df = BCRP.get_data(
    series={'PN02526AQ':'PBI'},
    fechaini='2000Q1',
    fechafin='2023Q2'
)

df
```

```text
             PBI
2001Q1 -5.330526
2001Q2  0.301282
2001Q3  2.742307
2001Q4  4.782608
2002Q1  6.525020
         ...
2022Q2  3.370007
2022Q3  1.956069
2022Q4  1.661968
2023Q1 -0.408395
2023Q2 -0.495679

[90 rows x 1 columns]
```


### Ejemplo: Extracción de datos de Banco Mundial
Iniciaremos con la consulta del _PBI per cápita en PPP constantes (US$ 2017)_ para Perú, Chile y Colombia:

```python
from econdata import WB

WB.search(
    consulta=['gdp', 'per', 'capita']
)
```

```text
id                                                                  
NY.GDP.PCAP.CD                          GDP per capita (current US$)
NY.GDP.PCAP.CN                          GDP per capita (current LCU)
NY.GDP.PCAP.KD                    GDP per capita (constant 2015 US$)
NY.GDP.PCAP.KD.ZG                   GDP per capita growth (annual %)
NY.GDP.PCAP.KN                         GDP per capita (constant LCU)
NY.GDP.PCAP.PP.CD      GDP per capita, PPP (current international $)
NY.GDP.PCAP.PP.KD  GDP per capita, PPP (constant 2017 internation...
PA.NUS.PPP         PPP can be used to convert national accounts d...
PA.NUS.PRVT.PP     PPP can be used to convert national accounts d...
SE.XPD.PRIM.PC.ZS  Government expenditure per student, primary (%...
SE.XPD.SECO.PC.ZS  Government expenditure per student, secondary ...
SE.XPD.TERT.PC.ZS  Government expenditure per student, tertiary (...
```

Tras obtener el código de la serie (```NY.GDP.PCAP.PP.KD```), se puede solicitar la data para un rango de periodos:

```python
df = WB.get_data(
    {
        'CO': 'Colombia',
        'CL': 'Chile',
        'PE': 'Perú'
    },
    indicator = 'NY.GDP.PCAP.PP.KD',
    fechaini = '2012',
    fechafin = '2022'
)

df
```

```text
          Colombia         Chile          Perú
time                                          
2012  12934.965752  23467.978726  11084.873937
2013  13465.075044  24011.591014  11620.644447
2014  13938.231517  24197.183280  11773.944135
2015  14215.688252  24464.745662  12015.187156
2016  14358.168218  24599.374633  12321.318154
2017  14334.914608  24546.912421  12442.746462
2018  14426.434382  25071.990069  12696.236289
2019  14616.135124  24809.860974  12735.168278
2020  13358.298083  22970.550435  11187.343790
2021  14661.213244  25412.752073  12533.841417
2022  15651.582058  25886.121356  12743.942391
```


### Ejemplo: Extracción de datos de Yahoo! Finance
Iniciaremos con la consulta de la cotización de _Apple_ y _Microsoft_:

```python
from econdata import YFinance

YFinance.search(
    consulta=['Microsoft']
)
```

```text
                                      Name        Country  IPO Year  \
Symbol                                                                
MSFT    Microsoft Corporation Common Stock  United States      1986   

            Sector                                 Industry  
Symbol                                                       
MSFT    Technology  Computer Software: Prepackaged Software
```

Tras obtener el Ticker de las series (```AAPL``` y ```MSFT```), se puede solicitar la data para un rango de periodos:

```python
df = YFinance.get_data(
    {
        'AAPL': 'Apple',
        'MSFT': 'Microsoft'
    },
    fechaini = '2018-01-01',
    fechafin = '2023-10-15'
)

df
```

```text
                 Apple   Microsoft
Date                              
2018-01-02   40.776524   80.391853
2018-01-03   40.769421   80.765976
2018-01-04   40.958794   81.476830
2018-01-05   41.425129   82.487007
2018-01-08   41.271259   82.571159
               ...         ...
2023-10-09  178.990005  329.820007
2023-10-10  178.389999  328.390015
2023-10-11  179.800003  332.420013
2023-10-12  180.710007  331.160004
2023-10-13  178.850006  327.730011

[1456 rows x 2 columns]
```


## Contenido adicional
Para más información revisar los siguientes links:
* Más códigos de _test_ están disponibles [aquí](https://github.com/mauricioalvaradoo/econdata/blob/master/test.py).
* El video del anuncio de la librería y la demo está disponible [aquí](https://www.youtube.com/watch?v=etaqHMDfvtE).
* Revisar un proyecto de la creación de un dashboard de indicadores peruanos elaborado con la librería, disponible [aquí](https://github.com/mauricioalvaradoo/indicators).


## Créditos
* [Mauricio Alvarado](https://github.com/mauricioalvaradoo). email: mauricio.alvarado@pucp.edu.pe
* [Andrei Romero](https://github.com/Ixtalia)

