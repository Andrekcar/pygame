import pygame
from pygame import *
import math
import time # librerias necesarias

# pygame init
pygame.init()

# ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 580
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
pygame.display.set_caption("TASK 5")

clock = pygame.time.Clock()
running = True
dt = 0

# Cargar y escalar las imágenes
fondo = image.load('assets/images/fondo.png')
fondo = transform.scale(fondo, (WINDOW_WIDTH, WINDOW_HEIGHT))  # fondo 

pelota = image.load('assets/images/pelota.png')
pelota = transform.scale(pelota, (30, 30))  # pelota

cubo1 = image.load('assets/images/cubo.png')
cubo1 = transform.scale(cubo1, (50, 50))  # cubo1

cubo2 = image.load('assets/images/cubo.png')
cubo2 = transform.scale(cubo2, (50, 50))  # cubo2

# Cargar bolas inamovibles (obstáculos)
balls = []
for i in range(1, 11):
    ball = image.load(f'assets/images/ball{i}.png')
    ball = transform.scale(ball, (65, 65))
    balls.append(ball) # por cada iteracion se cargan las imagenes en el dicionario

# Posiciones fijas para las bolas inamovibles
ball_positions = [
    pygame.Vector2(400, 90 + i * 50) for i in range(len(balls)) 
] 

# Posición inicial pelota
player_pos = pygame.Vector2((125, 500))

# Tamaños
PLAYER_SIZE = 15 
BALL_SIZE = 30  

# Variables del cronómetro
start_time = None
elapsed_time = 0
game_started = False

# Punto B (posición del cubo2)
goal_pos = pygame.Vector2(675, 525) 

# Función para formatear el tiempo en mm:ss
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Verificar colisión entre dos círculos
def check_collision(pos1, pos2, radius1, radius2):
    distance = math.sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)
    return distance < (radius1 + radius2) # valida la distancia entre radios para detectar una zona de colision 

# Verificar si el jugador alcanza el punto objetivo
def check_goal(player_pos, goal_pos, radius):
    """Verifica si el jugador ha llegado al punto objetivo."""
    distance = math.sqrt((player_pos.x - goal_pos.x)**2 + (player_pos.y - goal_pos.y)**2)
    return distance < radius

# colisiones con bolas obstaculo
def balls_collision(player_pos, ball_pos):
    collision_vector = pygame.Vector2(player_pos.x - ball_pos.x, player_pos.y - ball_pos.y)
    if collision_vector.length() > 0:
        collision_vector = collision_vector.normalize()
        correction = (PLAYER_SIZE + BALL_SIZE) - collision_vector.length()
        player_pos.x = ball_pos.x + collision_vector.x * (PLAYER_SIZE + BALL_SIZE)
        player_pos.y = ball_pos.y + collision_vector.y * (PLAYER_SIZE + BALL_SIZE)
    return player_pos

# Mostrar ventana de "Ganaste"
def win_screen():
    win_screen = True
    font = pygame.font.Font(None, 50)
    while win_screen:
        screen.fill((0, 0, 0))
        # Primera línea del mensaje
        win_text1 = font.render("Objetivo Alcanzado!", True, (255, 255, 255))
        # Segunda línea del mensaje
        win_text2 = font.render("¿Reiniciar el juego? [S/N]", True, (255, 255, 255))
        # Mostrar primera línea
        screen.blit(win_text1, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        # Mostrar segunda línea
        screen.blit(win_text2, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 10))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Reiniciar el juego
                    return True
                if event.key == pygame.K_n:  # Salir del juego
                    pygame.quit()
                    exit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el fondo
    screen.blit(fondo, (0, 0))

    # Manejar movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
        if not game_started:
            game_started = True
            start_time = time.time()
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
        if not game_started:
            game_started = True
            start_time = time.time()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
        if not game_started:
            game_started = True
            start_time = time.time()
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        if not game_started:
            game_started = True
            start_time = time.time()

    # Aplica colisiones con los bordes de la ventana
    if player_pos.x < PLAYER_SIZE:
        player_pos.x = PLAYER_SIZE
    if player_pos.x > WINDOW_WIDTH - PLAYER_SIZE:
        player_pos.x = WINDOW_WIDTH - PLAYER_SIZE
    if player_pos.y < PLAYER_SIZE:
        player_pos.y = PLAYER_SIZE
    if player_pos.y > WINDOW_HEIGHT - PLAYER_SIZE:
        player_pos.y = WINDOW_HEIGHT - PLAYER_SIZE

    # Verificar colisiones con las bolas inamovibles
    for ball_pos in ball_positions:
        if check_collision(player_pos, ball_pos, PLAYER_SIZE, BALL_SIZE):
            player_pos = balls_collision(player_pos, ball_pos)

    # Verificar si el jugador alcanzó el punto objetivo
    if game_started and check_goal(player_pos, goal_pos, PLAYER_SIZE):
        elapsed_time = time.time() - start_time
        game_started = False
        if win_screen():  # Mostrar ventana de ganaste y reiniciar si elige "S"
            player_pos = pygame.Vector2((125, 500))  # Reiniciar posición del jugador
            start_time = None
            elapsed_time = 0
            game_started = False

    # Dibujar las bolas inamovibles
    for index, ball in enumerate(balls):
        ball_x = ball_positions[index].x - BALL_SIZE
        ball_y = ball_positions[index].y - BALL_SIZE
        screen.blit(ball, (ball_x, ball_y))

    # Dibujar la bola del jugador
    screen.blit(pelota, (player_pos.x - PLAYER_SIZE, player_pos.y - PLAYER_SIZE))

    # Dibujar los cubos
    screen.blit(cubo1, (100, 500))  # Punto A
    screen.blit(cubo2, (650, 500))  # Punto B

    # Mostrar el cronómetro y nombre
    if game_started:
        current_time = time.time() - start_time
    else:
        current_time = elapsed_time

    time_text = format_time(current_time)
    time_surface = pygame.font.Font(None, 36).render(
        f"Tiempo: {time_text} | Autor: Andrès Camilo Caro", True, (255, 255, 255)
    )
    screen.blit(time_surface, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar FPS a 60 y calcular el delta time
    dt = clock.tick(60) / 1000

pygame.quit()
