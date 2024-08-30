import sys
import math
import random

# Fase de inicialización
p, _id, d, z = map(int, input().split())
zones = [tuple(map(int, input().split())) for _ in range(z)]

# Función para calcular la distancia euclidiana
def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

# Función para predecir el movimiento de los drones enemigos
def predict_enemy_movement(current_enemy_drones):
    if len(enemy_history) > 1:
        last_positions = enemy_history[-1]
        return [(current[0] + (current[0] - last[0]), current[1] + (current[1] - last[1]))
                for current, last in zip(current_enemy_drones, last_positions)]
    return current_enemy_drones

# Función para asignar roles (atacantes/defensores) a los drones según el progreso del juego
def assign_roles(my_drones, game_progress):
    num_attackers = max(1, min(d, int(d * (0.7 - game_progress * 0.4))))
    return my_drones[:num_attackers], my_drones[num_attackers:]

# Función para encontrar la mejor zona a la que apuntar
def find_best_zone(drone, controlled_zones, enemy_drones, my_drones):
    mejor_zona = None
    mejor_puntuacion = float('inf')

    for i, zona in enumerate(zones):
        puntuacion_zona = distance(drone[0], drone[1], zona[0], zona[1])

        cantidad_enemigos = sum(1 for enemigo in enemy_drones if distance(enemigo[0], enemigo[1], zona[0], zona[1]) < 100)
        cantidad_aliados = sum(1 for aliado in my_drones if distance(aliado[0], aliado[1], zona[0], zona[1]) < 100)

        if controlled_zones[i] == -1:
            puntuacion_zona -= 150  # Capturar zonas no ocupadas es más importante
        elif controlled_zones[i] == _id:
            puntuacion_zona += 250  # Evitar perder tiempo en zonas ya controladas

        puntuacion_zona += (cantidad_enemigos * 60) - (cantidad_aliados * 40)  # Ajustar según la presencia de drones

        if puntuacion_zona < mejor_puntuacion:
            mejor_puntuacion = puntuacion_zona
            mejor_zona = zona

    return mejor_zona

# Función para calcular las posiciones de destino para los drones
def calculate_target_positions(my_drones, attackers, defenders, controlled_zones, predicted_enemies):
    objetivos = {}

    # Formación en triángulo para los primeros tres atacantes
    if len(attackers) >= 3:
        lider = attackers[0]
        seguidores = attackers[1:3]
        angulo_offset = 2 * math.pi / 3
        for i, seguidor in enumerate(seguidores):
            angulo = angulo_offset * i
            x = int(my_drones[lider][0] + math.cos(angulo) * 50)
            y = int(my_drones[lider][1] + math.sin(angulo) * 50)
            objetivos[seguidor] = (x, y)
        objetivos[lider] = zones[random.randint(0, z - 1)]  # El líder va hacia una zona aleatoria

    # Asignar los demás atacantes a la mejor zona
    for atacante in attackers[3:]:
        objetivos[atacante] = find_best_zone(my_drones[atacante], controlled_zones, predicted_enemies, my_drones)

    # Los defensores se quedan en las zonas controladas más cercanas
    for defensor in defenders:
        zona_mas_cercana = min((zona for zona, controlador in enumerate(controlled_zones) if controlador == _id),
                               key=lambda i: distance(my_drones[defensor][0], my_drones[defensor][1], zones[i][0], zones[i][1]))
        objetivos[defensor] = zones[zona_mas_cercana]

    # Añadir un poco de aleatoriedad para confundir al enemigo
    if len(my_drones) > 5 and random.random() < 0.1:
        señuelo = random.choice(list(objetivos.keys()))
        objetivos[señuelo] = (random.randint(0, 4000), random.randint(0, 1800))

    return objetivos

# Bucle principal del juego
enemy_history = []
turn = 0

while True:
    turn += 1
    progreso_juego = min(turn / 200, 1)

    # Leer datos de entrada
    controlled_zones = [int(input()) for _ in range(z)]
    drones = [tuple(map(int, input().split())) for _ in range(p * d)]
    my_drones = drones[_id * d:(_id + 1) * d]
    enemy_drones = [drone for i, drone in enumerate(drones) if i // d != _id]

    # Guardar posiciones enemigas
    enemy_history.append(enemy_drones)
    if len(enemy_history) > 5:
        enemy_history.pop(0)

    # Predecir movimientos enemigos
    enemigos_predichos = predict_enemy_movement(enemy_drones)

    # Asignar roles a los drones
    atacantes, defensores = assign_roles(list(range(d)), progreso_juego)

    # Calcular posiciones de destino
    objetivos = calculate_target_positions(my_drones, atacantes, defensores, controlled_zones, enemigos_predichos)

    # Mover drones a las posiciones de destino
    for i in range(d):
        objetivo = objetivos.get(i, (2000, 900))  # Por defecto, ir al centro del mapa
        actual = my_drones[i]
        dx, dy = objetivo[0] - actual[0], objetivo[1] - actual[1]
        dist = math.hypot(dx, dy)
        if dist > 100:
            dx, dy = int(dx / dist * 100), int(dy / dist * 100)
        print(f"{actual[0] + dx} {actual[1] + dy}")

    # Salida (para ver qué está haciendo el código
    #print(f"Turno {turn}, Zonas: {controlled_zones}", file=sys.stderr, flush=True)
    #print(f"Atacantes: {atacantes}, Defensores: {defensores}", file=sys.stderr, flush=True)

    # Coipo: Si bn es util mirar, descubri cque el debugmode de de la misma pag muestra de forma simplificada los movimientos de los drones, deberia quitarlo!
