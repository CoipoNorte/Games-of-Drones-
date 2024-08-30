import sys
import math

# Datos de iniciales señore
p, _id, d, z = [int(i) for i in input().split()]
zones = []
for i in range(z):
    x, y = [int(j) for j in input().split()]
    zones.append((x, y))

# Calcular la distancia entre dos puntos (sqrt: )
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Zona mas cercana no controlada / controlada por un enemigo
def find_best_zone(drone, controlled_zones, enemy_drones):
    best_zone = None
    best_score = float('inf')
    for i, zone in enumerate(zones):
        if controlled_zones[i] != _id:
            zone_score = distance(drone[0], drone[1], zone[0], zone[1])
            # Penalizamos zonas con muchos drones enemigos cerca
            for enemy in enemy_drones:
                if distance(enemy[0], enemy[1], zone[0], zone[1]) < 200:
                    zone_score += 50
            if zone_score < best_score:
                best_score = zone_score
                best_zone = zone
    return best_zone

# Esto era el gameloop pero me gusta pensar que es el main
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
    
    # Asignar -> objetivo a dron
    targets = {}
    for i, drone in enumerate(my_drones):
        best_zone = find_best_zone(drone, controlled_zones, enemy_drones)
        if best_zone:
            targets[i] = best_zone
    
    # Mover -> drones a objetivo
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
            # Movemos dron a centro
            print("2000 900")
    
    print("VARIABLE: controlled_zones:", controlled_zones, file=sys.stderr, flush=True)
    print("VARIABLE: targets:", targets, file=sys.stderr, flush=True)