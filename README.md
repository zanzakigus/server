# Server del TT 2021-A028

Para el desarrollo dela Trabajo Terminal, de la Escuela Superior de C贸mputo del Instituto Polit茅cnico Nacional, antes mencionado,
se desarrolla este servidor para poder realizar las funcionalidades de conexiones a la base de datos, asi como manejo de las redes neuronales.

## Comenzando 馃殌

A continuaci贸n se menciona el procedimiento que se debe de llevar a cabo para arrancar el servidor.

Mira **Despliegue** para conocer como desplegar el proyecto.

### Pre-requisitos 馃搵

Las tecnolog铆as necesarias para poder correr el servidor se encuentran descritas en el archivo requirements.txt

### Instalaci贸n 馃敡

Se requiere la descarga de este mismo repositorio.

```
git clone https://github.com/zanzakigus/server.git

Instalar pip de python:

sudo apt install python3-pip
```

Entrar a la carpeta del proyecto y correr el comando siguiente en consola:

```
pip install -r requirements.txt
```

Creaci贸n y/o actualizaci贸n de base de datos

```
cd others
python init.py
```

## Ejecutando el servidor 鈿欙笍

Para correr el servidor usar el comandando siguiente en consola:

```
flask run
```

Para correr el servidor con ip detectable red interna ejecutar el comandando siguiente en consola:

```
flask run -h 0.0.0.0 -p 8000
```

Verificar que el puesto 8000 este abierto

## Despliegue 馃摝

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 馃洜锔?

_Menciona las herramientas que utilizaste para crear tu proyecto_

- [Pycharm](https://www.jetbrains.com/pycharm/) - Uno de los IDEs mas poderosos
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Para el desarrollo web con python

## Autores 鉁掞笍

Se agradece la participaci贸n de los siguientes mencionados que ayudaron a la realizaci贸n de este proyecto.

- **Daniel Covarrubias** - [Cova-ops](https://github.com/Cova-ops)
- **Erick Rodriguez** - [zanzakigus](https://github.com/zanzakigus)
- **Diego Flores** - [diego_flores](#DiegoTuGit)

## Licencia 馃搫

MIT
