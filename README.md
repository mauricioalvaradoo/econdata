# Econdata
Extracción de series de tiempo de las principales instituciones económicas para el Perú:
1. Banco Central de Reserva del Perú (BCRP)
2. Yahoo Finance
3. Federal Reserve Economic Data (FRED)
4. World Bank
5. Organización para la Cooperación y el Desarrollo Económicos (OCDE)

```
# Instalación mediante PyPI
!pip install econdata==1.0.3

# o simplemente:
!pip install econdata
```
El anuncio fue realizado en Linkedin, y está disponible [aquí](https://www.linkedin.com/posts/mauricioalvaradoo_github-mauricioalvaradooecondata-extracci%C3%B3n-activity-7053798889950179328-wl5w?utm_source=share&utm_medium=member_desktop). 


## Versión 1.0.3
* Para el `BCRP`, `Yahoo Finance`, `FRED` y el `World Bank`, se cuenta con ambos métodos: `get_data()` y `search()`.
* Para la `OCDE`, se cuenta únicamente con el método `get_data()`.
* En la versión 1.0.3, (i) se corrigió el formato de las fechas para `BCRP` y `FRED`, y (ii) se añadió el filtro de frecuencia en `search()` para `FRED`.


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


## Créditos
* [Mauricio Alvarado](https://github.com/mauricioalvaradoo)
* [Andrei Romero](https://github.com/Ixtalia)

