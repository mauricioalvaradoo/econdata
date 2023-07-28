# Econdata
Extracción de series de tiempo de las principales instituciones económicas para el Perú:
1. Banco Central de Reserva del Perú (BCRP)
2. Yahoo Finance (YFinance)
3. Federal Reserve Economic Data (FRED)
4. World Bank (WB)
5. Organization for Economic Cooperation and Development (OECD)
6. International Monetary Fund (IMF)

```
# Instalación mediante PyPI
!pip install econdata==1.0.6

# o simplemente:
!pip install econdata
```
El anuncio fue realizado en Linkedin, y está disponible [aquí](https://www.linkedin.com/posts/mauricioalvaradoo_github-mauricioalvaradooecondata-extracci%C3%B3n-activity-7053798889950179328-wl5w?utm_source=share&utm_medium=member_desktop). 


## Versión 1.0.6
* Para el `BCRP`, `YFinance`, `FRED`, `IMF` y el `WB`, se cuenta con ambos métodos: `get_data()` y `search()`.
* Para la `OECD`, se cuenta únicamente con el método `get_data()`.
* En la versión 1.0.6, se incluyó el `IMF`.


## Métodos
Para cada institución se tiene dos métodos comunes. El primero sirve para extraer las series dado un rango de peridos:
```
get_data()
```

La segunda sirve para conseguir la metadata:
```
search()
```
El resultado incluye los nombres, códigos y fechas que servirán como complemento con la función anterior: `get_data()`.


## Test !
El código guía para usar las funciones está disponible [aquí](https://github.com/mauricioalvaradoo/econdata/blob/master/test.py).
El video del anuncio de la librería y la demo está disponible [aquí](https://www.youtube.com/watch?v=etaqHMDfvtE).

Además, revisar un proyecto de la creación de un dashboard de indicadores peruanos elaborado con la librería, disponible [aquí](https://github.com/mauricioalvaradoo/indicators).



## Créditos
* [Mauricio Alvarado](https://github.com/mauricioalvaradoo)
* [Andrei Romero](https://github.com/Ixtalia)

