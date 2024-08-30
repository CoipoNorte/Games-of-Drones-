import sys
import math

# Leemos los datos de inicialización
p, _id, d, z = [int(i) for i in input().split()]
zones = []
for i in range(z):
    x, y = [int(j) for j in input().split()]
    zones.append((x, y))

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_best_zone(drone, controlled_zones, enemy_drones, my_drones):
    best_zone = None
    best_score = float('inf')
    for i, zone in enumerate(zones):
        zone_score = distance(drone[0], drone[1], zone[0], zone[1])
        
        # Factores adicionales para la puntuación
        enemy_count = sum(1 for enemy in enemy_drones if distance(enemy[0], enemy[1], zone[0], zone[1]) < 200)
        ally_count = sum(1 for ally in my_drones if distance(ally[0], ally[1], zone[0], zone[1]) < 200)
        
        # Priorizamos zonas no controladas
        if controlled_zones[i] == -1:
            zone_score -= 100
        # Penalizamos zonas controladas por nosotros
        elif controlled_zones[i] == _id:
            zone_score += 200
        # Ajustamos la puntuación basada en la presencia de aliados y enemigos
        zone_score += enemy_count * 50 - ally_count * 30
        
        if zone_score < best_score:
            best_score = zone_score
            best_zone = zone
    return best_zone

def assign_roles(my_drones, controlled_zones):
    attackers = []
    defenders = []
    for i, drone in enumerate(my_drones):
        if any(controlled_zones[j] == _id and distance(drone[0], drone[1], zones[j][0], zones[j][1]) < 150 for j in range(z)):
            defenders.append(i)
        else:
            attackers.append(i)
    return attackers, defenders

# game loop
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
    
    # Asignamos roles a los drones
    attackers, defenders = assign_roles(my_drones, controlled_zones)
    
    # Asignamos objetivos a cada dron
    targets = {}
    for i in attackers:
        best_zone = find_best_zone(my_drones[i], controlled_zones, enemy_drones, my_drones)
        if best_zone:
            targets[i] = best_zone
    
    # Comportamiento de defensa
    for i in defenders:
        closest_controlled_zone = min(
            (j for j in range(z) if controlled_zones[j] == _id),
            key=lambda j: distance(my_drones[i][0], my_drones[i][1], zones[j][0], zones[j][1])
        )
        targets[i] = zones[closest_controlled_zone]
    
    # Movemos los drones hacia sus objetivos
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
            # Si no hay objetivo, movemos el dron hacia el centro
            print("2000 900")
    
    print(f"Debug: Controlled zones: {controlled_zones}", file=sys.stderr, flush=True)
    print(f"Debug: Targets: {targets}", file=sys.stderr, flush=True)
    print(f"Debug: Attackers: {attackers}, Defenders: {defenders}", file=sys.stderr, flush=True)