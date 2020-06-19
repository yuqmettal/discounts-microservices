# Arquitectura del proyecto 📏

_El proyecto ha sido rediseñado de su arquitectura inicial (monolitica) a una arquitectura de microservicios._

El proyecto consta de cinco servicios, los cuales para su despliegue son orquestados con docker compose. A continuacion se listan los servicios y un en lace a la documentacion de cada uno:

* [Servidor Eureka](/eureka-server/README.md)
* [Servicio de Direcciones](/address-service/README.md)
* [Servicio de Partners](/partners-service/README.md)
* [Servicio de Items](/items-service/README.md)
* [Servicio de Ordenes](/orders-service/README.md)

## Modelo inicial del proyecto 👴

A continuacion se muestra el modelo inicial del sistema.

![Modelo antiguo](/old_model.jpg)

## Dividiendo el monolito ✂️

Con el fin de simplificar el desarrollo de nuevas funcionalidades del proyecto, es necesario dividir toda la solucion en microservicios, lo cual a futuro tambien nos brindara la posibilidad de escalamiento vertical.

Se ha dividido el monolito en cuatro servicios basados en las responsabilidades que cumplen.

Los servicios son: 

* [Servicio de Direcciones](/address-service/README.md)
* [Servicio de Partners](/partners-service/README.md)
* [Servicio de Items](/items-service/README.md)
* [Servicio de Ordenes](/orders-service/README.md)

![Servicios](/Services.png)

Cada servicio posee responsabilidades unicas y trabaja con una base de datos independiente de los otros servicios.

Como es de suponer, los servicios estan relacionados. A continuacion un esquema de la relacion entre los servicios:

![Relaciones](/service_dependences.png)


## Comunicacion entre servicios ☎️

Segun lo visto en el apartado anterior, hemos partido el monolito en servicios, pero ahora, necesitamos que los servicios se comuniquen entre si para entre otras cosas validar la integridad de los datos.

Esto quiza nos agregue complejidad al establecer las comunicaciones entre los servicios, lo cual empeorara cuando queramos escalar un servicio.

Para esto se ha hecho uso del patron arquitectonico **Discovery server** implementado por Eureka, el mismo que brinda tambien balanceo de carga lo cual nos interesa ya que esperamos en algun momento escalar un servicio altamente demandado.
A continuacion la documentacion del servicio eureka:

* [Servicio Eureka](/eureka-server/README.md)

Al implementar Eureka tenemos un panorama distinto, ahora podemos comunicar efectivamente los servicios y el tema de escalamiento de servicios es mucho mas facil y nuestro diseño queda de la siguiente manera:

![Services](/service_discovery.png)

#### Voila! 🎉🎉🎉

Hemos implementado una arquitectura basica de microservicios perfectamente escalable!!!
