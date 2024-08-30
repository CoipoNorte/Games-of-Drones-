# Games-of-Drones-
Solucion maoma a Games of Drones un desafio de Coding Games creo

## Descripcion
Esta estrategia se enfoca en el control y la gestión de zonas en un entorno de juego utilizando drones.

### Almacenamiento Inicial de Información

- **Al inicio del juego**, almacenamos la información de las zonas disponibles. (Buena practica segun papas fritas)

### Proceso por Turno OJO PIOJO

1. **Actualización del Estado de Control de Zonas**
   - Se actualiza el estado de control de cada zona para reflejar los cambios recientes. (Como mirar el mapa)

2. **Obtencion de Posiciones de Drones**
   - Se obtienen las posiciones actuales de todos los drones, tanto nuestros como enemigos. (Saber es poder)

3. **Asignacion de Objetivos a Nuestros Drones**
   - Para cada uno de nuestros drones:
     - **Búsqueda de la Mejor Zona Objetivo**
       - Utilizamos la función `find_best_zone` para determinar la mejor zona objetivo. 
       - Consideramos zonas que no estan controladas o que estan controladas por enemigos.
       - Calculamos una puntuacion basada en la distancia a la zona.
       - Penalizamos las zonas que tienen una alta concentración de drones enemigos cercanos.
     - **Movimiento hacia el Objetivo**
       - Si el objetivo está a ams de 100 unidades de distancia, movemos el dron 100 unidades en esa direccion.
       - Si no hay zonas disponibles (todas las zonas están controladas), movemos el dron hacia el centro del mapa. (de alli es mas facil llegar a todos lados creo yo)

4. **Mensajes de consola**
   - Añadimos mensajes para visualizar el estado actual de las zonas controladas y los objetivos de nuestros drones. (por mas que veo la pantalla me cuesta distingir el rojo del naranja :(( )

5. **Captura de Pantalla mi gente**
## Imagen de la pag

![Estrategia de Control de Zonas](gameofdrones.png)

