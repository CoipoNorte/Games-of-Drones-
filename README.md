# Games-of-Drones-
Solucion maoma a Games of Drones un desafio de Coding Games creo

## Descripcion
Esta estrategia se enfoca en el control y la gestión de zonas en un entorno de juego utilizando drones.

Este código implementa una solución para el juego descrito, donde el objetivo es controlar zonas en un mapa utilizando drones. El juego se desarrolla por turnos, y cada jugador dirige varios drones para capturar y mantener el control de las zonas. A continuación, te explico el código y su funcionamiento en detalle:

1. Lectura de Datos Iniciales
python
Copiar código
p, _id, d, z = [int(i) for i in input().split()]
zones = []
for i in range(z):
    x, y = [int(j) for j in input().split()]
    zones.append((x, y))
p: Número de jugadores.
_id: ID del jugador actual.
d: Número de drones por equipo.
z: Número de zonas en el mapa.
Aquí se almacena la información inicial sobre las zonas, guardando las coordenadas de cada zona en la lista zones.

2. Función de Distancia
python
Copiar código
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
Esta función calcula la distancia euclidiana entre dos puntos (x1, y1) y (x2, y2). Se utiliza para determinar qué tan lejos están los drones de las zonas y entre ellos.

3. Función para Buscar la Mejor Zona
python
Copiar código
def find_best_zone(drone, controlled_zones, enemy_drones, my_drones):
    best_zone = None
    best_score = float('inf')
    for i, zone in enumerate(zones):
        zone_score = distance(drone[0], drone[1], zone[0], zone[1])
        
        enemy_count = sum(1 for enemy in enemy_drones if distance(enemy[0], enemy[1], zone[0], zone[1]) < 200)
        ally_count = sum(1 for ally in my_drones if distance(ally[0], ally[1], zone[0], zone[1]) < 200)
        
        if controlled_zones[i] == -1:
            zone_score -= 100
        elif controlled_zones[i] == _id:
            zone_score += 200
        
        zone_score += enemy_count * 50 - ally_count * 30
        
        if zone_score < best_score:
            best_score = zone_score
            best_zone = zone
    return best_zone
Objetivo: Esta función evalúa las zonas y determina cuál es la mejor para enviar un drone. La evaluación se basa en:
Distancia a la zona.
Número de enemigos y aliados cerca de la zona.
Si la zona está controlada o no.
El "mejor" puntaje (best_score) se obtiene minimizando la distancia a la zona y considerando la presencia de drones enemigos y aliados.

4. Asignación de Roles (Atacantes y Defensores)
python
Copiar código
def assign_roles(my_drones, controlled_zones):
    attackers = []
    defenders = []
    for i, drone in enumerate(my_drones):
        if any(controlled_zones[j] == _id and distance(drone[0], drone[1], zones[j][0], zones[j][1]) < 150 for j in range(z)):
            defenders.append(i)
        else:
            attackers.append(i)
    return attackers, defenders
Objetivo: Esta función divide los drones entre atacantes y defensores. Un drone se asigna como defensor si ya está cerca de una zona controlada por el jugador, y como atacante si no lo está.
5. Ciclo del Juego (Loop Principal)
python
Copiar código
while True:
    controlled_zones = []
    for i in range(z):
        tid = int(input())
        controlled_zones.append(tid)
    
    drones = [[] for _ in range(p)]
    for i in range(p):
        for j in range(d):
            dx, dy = [int(k) for k in input().split()]
            drones[i].append((dx, dy))
    
    my_drones = drones[_id]
    enemy_drones = [drone for i, team in enumerate(drones) if i != _id for drone in team]
    
    attackers, defenders = assign_roles(my_drones, controlled_zones)
    
    targets = {}
    for i in attackers:
        best_zone = find_best_zone(my_drones[i], controlled_zones, enemy_drones, my_drones)
        if best_zone:
            targets[i] = best_zone
    
    for i in defenders:
        closest_controlled_zone = min(
            (j for j in range(z) if controlled_zones[j] == _id),
            key=lambda j: distance(my_drones[i][0], my_drones[i][1], zones[j][0], zones[j][1])
        )
        targets[i] = zones[closest_controlled_zone]
    
    for i in range(d):
        if i in targets:
            target = targets[i]
            current = my_drones[i]
            dx = target[0] - current[0]
            dy = target[1] - current[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 100:
                dx = int(dx / dist * 100)
                dy = int(dy / dist * 100)
            print(f"{current[0] + dx} {current[1] + dy}")
        else:
            print("2000 900")
    
    print(f"Zonas controladas: {controlled_zones}", file=sys.stderr, flush=True)
    print(f"A donde van: {targets}", file=sys.stderr, flush=True)
    print(f"Atacantes: {attackers}, Defensores: {defenders}", file=sys.stderr, flush=True)
Este ciclo se repite en cada turno del juego:

Lectura del Estado Actual: Se lee qué zonas están controladas y las posiciones de todos los drones.
Asignación de Roles: Se decide qué drones atacarán y cuáles defenderán.
Determinación de Objetivos: Para cada drone, se decide hacia dónde debe moverse (zona objetivo).
Movimiento de Drones: Se calculan los movimientos de los drones y se imprimen las nuevas coordenadas.
Depuración: Se imprime información útil sobre el estado del juego en la consola de errores (sys.stderr) para ayudar a entender las decisiones del algoritmo.

5. **Captura de Pantalla mi gente**
## Imagen de la pag

![Estrategia de Control de Zonas](gameofdrones.png)

