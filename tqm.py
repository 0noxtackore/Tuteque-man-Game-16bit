import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("El formidable Tuteque-man")

# Colores
RED = (255, 0, 0)

# Cargar las imágenes del personaje
img_idle = pygame.image.load("img/TQM1.png")
img_idle = pygame.transform.scale(img_idle, (84, 140))

# Animaciones
run_frames = [
    pygame.transform.scale(pygame.image.load(f"img/TQM{i}.png"), (84, 140)) for i in range(2, 5)
]
jump_frames = [
    pygame.transform.scale(pygame.image.load(f"img/Jump/TQM{i}.png"), (84, 140)) for i in range(1, 3)
]
roll_frames = [
    pygame.transform.scale(pygame.image.load(f"img/Jump/V-{i}.png"), (84, 140)) for i in range(1, 4)
]
punch_frames = [
    pygame.transform.scale(pygame.image.load(f"img/punch/TQM1.png"), (100, 140)),
    pygame.transform.scale(pygame.image.load(f"img/punch/TQM2.png"), (100, 140))
]
add_punch_frames = [
    pygame.transform.scale(pygame.image.load(f"img/punch/TQM1.png"), (100, 140)),
    pygame.transform.scale(pygame.image.load(f"img/punch/TQM3.png"), (100, 140))
]
punch_down_frames = [
    pygame.transform.scale(pygame.image.load(f"img/punch_down/TQM1.png"), (100, 140)),
    pygame.transform.scale(pygame.image.load(f"img/punch_down/TQM2.png"), (100, 140))
]
add_punch_down_frames = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"img/punch_down/TQM1.png"), (100, 140)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"img/punch_down/TQM2.png"), (100, 140)), True, False)
]
climb_frames = [
    pygame.transform.scale(pygame.image.load(f"img/climb/TQM{i}.png"), (140, 140)) for i in range(1, 5)
]
kick_frames = [
    pygame.transform.scale(pygame.image.load(f"img/kick/TQM1.png"), (100, 140)),
    pygame.transform.scale(pygame.image.load(f"img/kick/TQM2.png"), (100, 140))
]
add_kick_frames = [
    pygame.transform.scale(pygame.image.load(f"img/kick/TQM3.png"), (100, 140))
]

# Animación de reposo
rest_frames = [
    pygame.transform.scale(pygame.image.load("img/TQM1.png"), (84, 140)),
    pygame.transform.scale(pygame.image.load("img/impact.png"), (84, 140))
]

down_frames = [
    pygame.transform.scale(pygame.image.load("img/impact.png"), (84, 140)),
]

down_add_frames = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load("img/impact.png"), (84, 140)), True, False),
]

# Variables del jugador
pos = [100, 500]
spd = 12
ground = 450
jump_spd = 0
grav = 0.5
jumping = False
jump = False  
facing_r = True
facing_l = False
jump_cnt = 0
attack_cnt = 0  

# Inicializar variables de animación
cur_frame = 0
anim_spd = 5
anim_cnt = 0
jump_frm = 0
rest_frm = 0
rest_anim_spd = 20
rest_anim_cnt = 0
flipping = False
flip_dur = 30
flip_timer = 0
flip_ang = 0
punching = False
kicking = False
kick_frm = 0
kick_anim_spd = 10
kick_anim_cnt = 0
punch_anim_cnt = 0  
punch_offset = 15
kick_offset = 15

# Contador de golpes
hit_cnt = 0
cur_punch_imgs = []
cur_kick_imgs = []

# Nueva variable is_down
is_down = False

# Variables para la animación de escalada
climb_frame = 0
climb_anim_spd = 10  
climb_anim_cnt = 0

# Variables para el ataque hacia abajo
punch_downing = False
punch_down_frm = 0

# Función para seleccionar un golpe aleatorio
def random_attack():
    attack_type = random.choice(['punch', 'punch_additional', 'kick', 'kick_additional'])
    if attack_type == 'punch':
        return punch_frames
    elif attack_type == 'punch_additional':
        return add_punch_frames
    elif attack_type == 'kick':
        return kick_frames
    elif attack_type == 'kick_additional':
        return add_kick_frames

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    running = False
    show_impact = False

    # Movimiento del jugador
    if keys[pygame.K_LEFT] and not punching and not kicking and not punch_downing:
        pos[0] -= spd  
        facing_r = False
        facing_l = True
        running = True
        
    elif keys[pygame.K_RIGHT] and not punching and not kicking and not punch_downing:
        pos[0] += spd  
        facing_r = True
        facing_l = False
        running = True

    # Activar impacto al presionar la tecla de abajo
    if keys[pygame.K_DOWN] and pos[1] == ground and not jumping:
        show_impact = True
        is_down = True  

    # Cambiar la posición de impacto al presionar arriba solo si is_down es True
    if keys[pygame.K_UP] and is_down:
        is_down = False  

    # Activar salto al presionar la tecla "X" solo si no está en down
    if keys[pygame.K_x] and not jumping and not is_down:
        jump_spd = -15
        jumping = True
        jump = True  
        jump_cnt += 1

        if jump_cnt % 2 == 0:
            flipping = True
            flip_timer = flip_dur
            flip_ang = 0

    # Activar ataque/patada al presionar la tecla "Z"
    if keys[pygame.K_z] and not jumping and not is_down and not punch_downing:
        attack_cnt += 1  
        if attack_cnt % 5 == 0 or attack_cnt % 3 == 0 or attack_cnt % 2 == 0:  
            kicking = True
            kick_frm = 0
            cur_kick_imgs = random_attack() 
        else:
            punching = True
            punch_frm = 0
            cur_punch_imgs = random_attack() 

    # Activar ataque hacia abajo al presionar "Z" mientras está en posición "down"
    if keys[pygame.K_z] and is_down and not punch_downing:
        punch_downing = True
        punch_down_frm = 0

    # Gravedad y movimiento vertical
    pos[1] += jump_spd
    if pos[1] < ground:
        jump_spd += grav
    else:
        if jumping:
            jumping = False
        pos[1] = ground
        jump_spd = 0
        jump = False  

    # Actualizar la animación de puño
    if punching:
        punch_anim_cnt += 1
        if punch_anim_cnt >= 5:
            punch_frm += 1
            punch_anim_cnt = 0
            if punch_frm >= len(cur_punch_imgs):
                punching = False
                punch_frm = 0

    # Actualizar la animación de patada
    if kicking:
        kick_anim_cnt += 1
        if kick_anim_cnt >= kick_anim_spd:
            kick_frm += 1
            kick_anim_cnt = 0
            if kick_frm >= len(cur_kick_imgs):
                kicking = False
                kick_frm = 0

    # Actualizar la animación de ataque hacia abajo
    if punch_downing:
        punch_anim_cnt += 1
        if punch_anim_cnt >= 5:
            punch_down_frm += 1
            punch_anim_cnt = 0
            if punch_down_frm >= len(punch_down_frames):
                punch_downing = False
                punch_down_frm = 0

    # Actualizar la animación de voltereta
    if flipping:
        flip_timer -= 1
        flip_ang += 12
        if flip_timer <= 0:
            flipping = False
            flip_ang = 0

    # Actualizar la animación de escalada
    if is_down:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            climb_anim_cnt += 1
            if climb_anim_cnt >= climb_anim_spd:
                climb_frame = (climb_frame + 1) % len(climb_frames)
                climb_anim_cnt = 0

    # Dibujar la pantalla
    screen.fill(RED)

    # Dibujar el personaje
    if is_down:  
        if keys[pygame.K_LEFT]:
            flipped_img = pygame.transform.flip(climb_frames[climb_frame], True, False)
            screen.blit(flipped_img, (pos[0], pos[1]))
        elif keys[pygame.K_RIGHT]:
            screen.blit(climb_frames[climb_frame], (pos[0], pos[1]))
        else:
            if punch_downing:
                if facing_r:
                    screen.blit(punch_down_frames[punch_down_frm], (pos[0], pos[1]))
                else:
                    screen.blit(add_punch_down_frames[punch_down_frm], (pos[0], pos[1]))
            else:
                # Cambiado para usar down_frames o down_add_frames según la dirección
                rest_anim_cnt += 1
                if rest_anim_cnt >= rest_anim_spd:
                    rest_frm += 1
                    rest_anim_cnt = 0
                    if rest_frm >= len(down_frames):
                        rest_frm = 0
                if facing_r:
                    screen.blit(down_frames[0], (pos[0], pos[1]))
                else:
                    screen.blit(down_add_frames[0], (pos[0], pos[1]))

    elif punching:
        punch_offset_val = punch_offset if facing_r else -punch_offset
        if facing_r:
            screen.blit(cur_punch_imgs[punch_frm], (pos[0] + punch_offset_val, pos[1]))
        else:
            flipped_img = pygame.transform.flip(cur_punch_imgs[punch_frm], True, False)
            screen.blit(flipped_img, (pos[0] + punch_offset_val, pos[1]))

    elif kicking:
        kick_offset_val = kick_offset if facing_r else -kick_offset
        if facing_r:
            screen.blit(cur_kick_imgs[kick_frm], (pos[0] + kick_offset_val, pos[1]))
        else:
            flipped_img = pygame.transform.flip(cur_kick_imgs[kick_frm], True, False)
            screen.blit(flipped_img, (pos[0] + kick_offset_val, pos[1]))

    elif jumping:
        if flipping:
            if facing_r:
                rotated_img = pygame.transform.rotate(roll_frames[jump_cnt % len(roll_frames)], flip_ang)
                rect = rotated_img.get_rect(center=(pos[0] + 42, pos[1] + 70))
                screen.blit(rotated_img, rect.topleft)
            else:
                rotated_img = pygame.transform.flip(pygame.transform.rotate(roll_frames[jump_cnt % len(roll_frames)], flip_ang), True, False)
                rect = rotated_img.get_rect(center=(pos[0] + 42, pos[1] + 70))
                screen.blit(rotated_img, rect.topleft)
        else:
            if facing_r:
                screen.blit(jump_frames[jump_frm], (pos[0], pos[1]))
            else:
                flipped_img = pygame.transform.flip(jump_frames[jump_frm], True, False)
                screen.blit(flipped_img, (pos[0], pos[1]))

            if jump_frm < len(jump_frames) - 1:
                jump_frm += 1

    elif pos[1] == ground:
        if running:
            if facing_r:
                screen.blit(run_frames[cur_frame], (pos[0], pos[1]))
            else:
                flipped_img = pygame.transform.flip(run_frames[cur_frame], True, False)
                screen.blit(flipped_img, (pos[0], pos[1]))

            anim_cnt += 1
            if anim_cnt >= anim_spd:
                cur_frame = (cur_frame + 1) % len(run_frames)
                anim_cnt = 0
        else:
            if show_impact:
                if facing_r:
                    screen.blit(down_frames[0], (pos[0], pos[1]))
                else:
                    screen.blit(down_add_frames[0], (pos[0], pos[1]))
            else:
                if facing_r:
                    screen.blit(rest_frames[0], (pos[0], pos[1]))
                else:
                    flipped_img = pygame.transform.flip(rest_frames[0], True, False)
                    screen.blit(flipped_img, (pos[0], pos[1]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
