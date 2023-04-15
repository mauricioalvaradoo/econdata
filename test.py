## Testeo
# !pip install econdata
from econdata import BCRP
from econdata import BM
from econdata import FRED
from econdata import OECD
from econdata import YFinance

import warnings
warnings.simplefilter("ignore")




## BCRP ====================================================
# search
consulta = BCRP.search(
    ["Interbancario"],
    grupo=["Tipo", "Cambio"],
    frecuencia="Mensual"
)
consulta

# get_data
df = BCRP.get_data(
    {
        "PN01207PM": "TC Interbancario promedio - pdp",
        "PN01205PM": "TC Interbancario compra - pdp",
        "PN01206PM": "TC Interbancario venta - pdp"
    },
    fechaini = "2000-01",
    fechafin = "2022-01"
)
df.head()

# get_documentation
doc = BCRP.documentation("PN01207PM")
doc




## Banco Mundial ===========================================
# search
consulta = BM.search(
    ["life", "expectancy"]
)
consulta

# get_data
df = BM.get_data(
    {
        "BR": "Brasil",
        "CL": "Chile",
        "PE": "Perú"
    },
    indicator = "SP.DYN.LE60.MA.IN", # Life expectancy at age 60, male
    fechaini = "1970",
    fechafin = "2022"
)
df.head()




## FRED ====================================================
# search
consulta = FRED.search(
    ["Gross", "Domestic", "Product"],
    api_key="#################################"
)
consulta

# get_data
df = FRED.get_data(
    {
        "GDPC1": "Real Gross Domestic Product s.a."
    },
    api_key="#################################",
    fechaini = "2000-01",
    fechafin = "2022-01"
)
df.head()




## OECD ====================================================
# search
df = OECD.get_data(
    identifier = "QNA", #Quarterly National Accounts
    countries = 
    {
        "AUS": "Australia",
        "AUT": "Austria",
        "BEL": "Belgica",
        "CAN": "Canada",
        "CHL": "Chile"
    },
    serie = "GDP+B1_GE.CUR+VOBARSA.Q", # Gross Domestic Product
    fechaini = "2004-Q1",
    fechafin = "2011-Q4",
    periodicidad = "Q"
)

df




## Yahoo Finance ===========================================
# search
consulta = YFinance.search(
    ["Tesla"]
)
consulta

# get_data 1 -> con fecha
df = YFinance.get_data(
    {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "TSLA": "Tesla"
    },
    fechaini = "2015-01-01",
    fechafin = "2022-12-31"
)
df.tail()

# get_data 2 -> sin fecha
df = YFinance.get_data(
    {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "TSLA": "Tesla"
    }
)
df.tail()

