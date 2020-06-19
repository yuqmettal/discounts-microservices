# Sistema de calculo de descuentos

_Proyecto para el calculo de descuentos basado en microservicios_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Despliegue** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_Que cosas necesitas para instalar el software y como instalarlas_

```
Docker
```


## Despliegue 📦

_Puedes desplegar el proyecto con docker compose_

Para ello, debes acceder al proyecto **deploy-discount-services** e ingresar el siguiente comando en la consola:

```
docker-compose up --build -d
```

Una vez ingresado el comando, los servicios tardaran en levantarse unos 5 minutos, dentro de lo cual ya estaran listos para trabajar. Ademas de esto, cada servicio tiene data precargada la cual se va ingresando a la base de datos de manera asincrona (Se pueden usar los servicios mientras se carga la data).


## Diseño 🔮

El proyecto ha sido diseñado con una arquitectura basada en microservicios.

Para mas detalle sobre el diseño ver [Arquitectura](Design.md).
 

## Uso 💻

Cada servicio ha sido documentado con OpenAPI en la cual se puede hacer peticiones. A continuacion los endpoints por defecto:

- [Address service](http://localhost:8001/docs) 
- [Partners service](http://localhost:8002/docs) 
- [Items service](http://localhost:8003/docs) 
- [Orders service](http://localhost:8004/docs) 


## Construido con 🛠️

* [Python 3.8](https://www.python.org/) - Lenguaje de programacion
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web
* [Uvicorn](https://www.uvicorn.org/) - Servidor de aplicaciones asicncrono basado en ASGI
* [Postgres](https://www.postgresql.org/) - Base de datos
* [Pytest](https://docs.pytest.org/en/stable/) - Framework de pruebas unitarias
* [Docker](https://www.docker.com/) - Contenedores para despliegue de aplicaciones

## Autor ✒️


* **Marco Yuquilima** - *Trabajo Inicial* - [yuqmettal](https://github.com/yuqmettal)