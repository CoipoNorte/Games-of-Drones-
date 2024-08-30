import sys
import math
import random

# Cosas del juego
p, _id, d, z = [int(i) for i in input().split()]
zones = []
for i in range(z):
    x, y = [int(j) for j in input().split()]
    zones.append((x, y))

# Cuanto de lejos estan las cosas
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Guardamos donde estaban los enemigos antes
enemy_history = []

# Adivinar donde van a ir los enemigos
def predict_enemy_movement(enemy_drones):
    if len(enemy_history) > 1:
        predictions = []
        for i, drone in enumerate(enemy_drones):
            dx = drone[0] - enemy_history[-1][i][0]
            dy = drone[1] - enemy_history[-1][i][1]
            predictions.append((drone[0] + dx, drone[1] + dy))
        return predictions
    return enemy_drones

# Formacion de drones como un triangulo
def triangle_formation(leader, followers):
    formation = [leader]
    angle = 0
    for follower in followers:
        x = leader[0] + int(math.cos(angle) * 50)
        y = leader[1] + int(math.sin(angle) * 50)
        formation.append((x, y))
        angle += 2 * math.pi / 3
    return formation

# Buscar la mejor zona para ir
def find_best_zone(drone, controlled_zones, enemy_drones, my_drones):
    best_zone = None
    best_score = float('inf')
    for i, zone in enumerate(zones):
        zone_score = distance(drone[0], drone[1], zone[0], zone[1])
        
        enemy_count = sum(1 for enemy in enemy_drones if distance(enemy[0], enemy[1], zone[0], zone[1]) < 200)
        ally_count = sum(1 for ally in my_drones if distance(ally[0], ally[1], zone[0], zone[1]) < 200)
        
        if controlled_zones[i] == -1:
            zone_score -= 150
        elif controlled_zones[i] == _id:
            zone_score += 250
        zone_score += enemy_count * 60 - ally_count * 40
        
        if zone_score < best_score:
            best_score = zone_score
            best_zone = zone
    return best_zone

# Decidir quien ataca y quien defiende
def assign_roles(my_drones, controlled_zones, game_progress):
    attackers = []
    defenders = []
    num_attackers = int(d * (0.7 - game_progress * 0.4))  # Mas defensores al final del juego
    for i, drone in enumerate(my_drones):
        if i < num_attackers:
            attackers.append(i)
        else:
            defenders.append(i)
    return attackers, defenders

# Aqui empieza el juego de verdad
turn = 0
while True:
    turn += 1
    game_progress = min(turn / 200, 1)  # El juego avanza

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
    
    # Guardamos donde estaban los enemigos
    enemy_history.append(enemy_drones)
    if len(enemy_history) > 5:
        enemy_history.pop(0)
    
    # Adivinamos donde van los enemigos
    predicted_enemies = predict_enemy_movement(enemy_drones)
    
    # Decidimos quien ataca y quien defiende
    attackers, defenders = assign_roles(my_drones, controlled_zones, game_progress)
    
    # A donde vamos
    targets = {}
    
    # Los atacantes van en formacion de triangulo
    if len(attackers) >= 3:
        leader = attackers[0]
        followers = attackers[1:3]
        formation = triangle_formation(my_drones[leader], [my_drones[f] for f in followers])
        for i, pos in zip([leader] + followers, formation):
            targets[i] = pos
    
    # Los demas atacantes buscan zonas
    for i in attackers[3:]:
        best_zone = find_best_zone(my_drones[i], controlled_zones, predicted_enemies, my_drones)
        if best_zone:
            targets[i] = best_zone
    
    # Los defensores se quedan en nuestras zonas
    for i in defenders:
        closest_controlled_zone = min(
            (j for j in range(z) if controlled_zones[j] == _id),
            key=lambda j: distance(my_drones[i][0], my_drones[i][1], zones[j][0], zones[j][1])
        )
        targets[i] = zones[closest_controlled_zone]
    
    # Un dron hace de señuelo si tenemos muchos
    if len(my_drones) > 5 and random.random() < 0.1:
        decoy = random.choice(list(targets.keys()))
        targets[decoy] = (random.randint(0, 4000), random.randint(0, 1800))
    
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
    print(f"Turno {turn}, Zonas: {controlled_zones}", file=sys.stderr, flush=True)
    print(f"Atacantes: {attackers}, Defensores: {defenders}", file=sys.stderr, flush=True)