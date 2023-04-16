# Econdata
Extracción de series de tiempo de las principales instituciones económicas para el Perú:
1. Banco Central de Reserva del Perú (BCRP)
2. Yahoo Finance
3. Federal Reserve Economic Data (FRED)
4. World Bank
5. Organización para la Cooperación y el Desarrollo Económicos (OCDE)

```
# Instalación mediante PyPI
!pip install econdata==1.0

# o simplemente:
!pip install econdata
```



## Versión 1.0
* Para el `BCRP`, `Yahoo Finance`, `FRED` y el `World Bank`, se cuenta con ambos métodos: `get_data()` y `search()`.
* Para la `OCDE`, se cuenta únicamente con el método `get_data()`.


## Métodos
Para cada institución se tiene dos métodos comunes. El primero sirve para extraer las series dado un rango de peridos:
```
get_data()
```

La segunda sirve para conseguir la metadata, principalmente, los códigos de las series:
```
search()
```
El resultado incluye los nombres, códigos y fechas que servirán como complemento con la función anterior: `get_data()`.


## Test !
El código guía para usar las funciones está disponible [aquí](https://github.com/mauricioalvaradoo/econdata/blob/master/test.py).


## Créditos
* [Mauricio Alvarado](https://github.com/mauricioalvaradoo)
* [Andrei Romero](https://github.com/Ixtalia)

