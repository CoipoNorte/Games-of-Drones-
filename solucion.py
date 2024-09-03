import sys
import math

# Leemos las cosas del juego
p, _id, d, z = [int(i) for i in input().split()]
zones = []
for i in range(z):
    x, y = [int(j) for j in input().split()]
    zones.append((x, y))

# Esta funcion dice que tan lejos estan las cosas
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Esta funcion busca la mejor zona para ir
def find_best_zone(drone, controlled_zones, enemy_drones, my_drones):
    best_zone = None
    best_score = float('inf')
    for i, zone in enumerate(zones):
        zone_score = distance(drone[0], drone[1], zone[0], zone[1])
        
        # Contamos cuantos amigos y enemigos hay cerca
        enemy_count = sum(1 for enemy in enemy_drones if distance(enemy[0], enemy[1], zone[0], zone[1]) < 200)
        ally_count = sum(1 for ally in my_drones if distance(ally[0], ally[1], zone[0], zone[1]) < 200)
        
        # Si nadie tiene la zona, es mejor
        if controlled_zones[i] == -1:
            zone_score -= 100
        # Si ya es nuestra, no es tan buena
        elif controlled_zones[i] == _id:
            zone_score += 200
        # Si hay muchos enemigos es mala, si hay amigos es buena
        zone_score += enemy_count * 50 - ally_count * 30
        
        if zone_score < best_score:
            best_score = zone_score
            best_zone = zone
    return best_zone

# Esta funcion dice que drones atacan y cuales defienden
def assign_roles(my_drones, controlled_zones):
    attackers = []
    defenders = []
    for i, drone in enumerate(my_drones):
        if any(controlled_zones[j] == _id and distance(drone[0], drone[1], zones[j][0], zones[j][1]) < 150 for j in range(z)):
            defenders.append(i)
        else:
            attackers.append(i)
    return attackers, defenders

# Aqui empieza el juego de verdad
while True:
    # Vemos quien controla cada zona
    controlled_zones = []
    for i in range(z):
        tid = int(input())
        controlled_zones.append(tid)
    
    # Vemos donde estan todos los drones
    drones = [[] for _ in range(p)]
    for i in range(p):
        for j in range(d):
            dx, dy = [int(k) for k in input().split()]
            drones[i].append((dx, dy))
    
    # Estos son nuestros drones y los de los enemigos
    my_drones = drones[_id]
    enemy_drones = [drone for i, team in enumerate(drones) if i != _id for drone in team]
    
    # Decidimos quien ataca y quien defiende
    attackers, defenders = assign_roles(my_drones, controlled_zones)
    
    # Buscamos a donde ir
    targets = {}
    for i in attackers:
        best_zone = find_best_zone(my_drones[i], controlled_zones, enemy_drones, my_drones)
        if best_zone:
            targets[i] = best_zone
    
    # Los que defienden se quedan en nuestras zonas
    for i in defenders:
        closest_controlled_zone = min(
            (j for j in range(z) if controlled_zones[j] == _id),
            key=lambda j: distance(my_drones[i][0], my_drones[i][1], zones[j][0], zones[j][1])
        )
        targets[i] = zones[closest_controlled_zone]
    
    # Movemos los drones a donde queremos que vayan
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
            # Si no sabemos que hacer, vamos al medio
            print("2000 900")
    
    # Esto es para ver que esta pasando
    print(f"Zonas controladas: {controlled_zones}", file=sys.stderr, flush=True)
    print(f"A donde van: {targets}", file=sys.stderr, flush=True)
    print(f"Atacantes: {attackers}, Defensores: {defenders}", file=sys.stderr, flush=True)
