import pygame, sys
import box

# Määritä värit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Määritä kenttä (0 = tyhjä, 1 = seinä, 2 = maali 3=laatikko)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 2, 1, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Määritä ruudun koko ja kentän leveys ja korkeus
BLOCK_SIZE = 75
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

# Määritä pelinäkymän koko
SCREEN_WIDTH = BLOCK_SIZE * MAP_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * MAP_HEIGHT

# Alusta Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban, Kodarit kesäohjelma 2024")

# Lataa kuvat

kodarit_img = pygame.image.load("kodarit.png")
kodarit_img = pygame.transform.scale(kodarit_img, (BLOCK_SIZE, BLOCK_SIZE))

kodarit_voitto_img = pygame.image.load("voittoruutu.png")
kodarit_voitto_img = pygame.transform.scale(kodarit_voitto_img, (BLOCK_SIZE * 12, BLOCK_SIZE * 8))

box_img = pygame.image.load("box.png")
box_img = pygame.transform.scale(box_img, (BLOCK_SIZE, BLOCK_SIZE))

player_img = pygame.image.load("dustball.png")
player_img = pygame.transform.scale(player_img, (BLOCK_SIZE, BLOCK_SIZE))

goal_img = pygame.image.load("goal.png")
goal_img = pygame.transform.scale(goal_img, (BLOCK_SIZE, BLOCK_SIZE))


wall_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
wall_img.fill("#00556f")

#Tähän kerätään kentällä olevien laatikoiden tiedot
boxes = []
#Tähän kerätään kentällä olevien maalien tiedot
goals = []

# Piirrä kenttä
def draw_floor_and_walls():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if MAP[y][x] == 1:
                screen.blit(wall_img, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            

#Luodaan kentälle maali Rectejä MAP-pelialuemäärityksen mukaan
def create_and_draw_goals():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
           if MAP[y][x] == 2:
                goal_rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                goals.append(goal_rect)
                screen.blit(goal_img, goal_rect)

#Piirretään maalit                
def draw_goals():
    for goal in goals:
        screen.blit(goal_img, goal)

#Luodaan kentälle laatikko-Rectejä MAP-pelialuemäärityksen mukaan
def create_and_draw_boxes():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if MAP[y][x] == 3:
                box_obj = box.Box(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE)
                boxes.append(box_obj)
                screen.blit(box_img, box_obj.rect)
                
#Piirretään laatikot kentälle               
def draw_boxes():
    for box in boxes:
        screen.blit(box_img, box.rect)

#Tarkistetaan onko laatikko jonkun maailn kanssa päällekkäin
def is_box_in_goal(box_rect):
    for goal in goals:
       if(box_rect.y == goal.y and box_rect.y == goal.y):
           print("laatikko maalissa ensimmäisen kerran")

#Tarkistetaan ovatko kaikki laatikot maalien päällä
def are_all_boxes_in_goals():
    all_goals = len(goals);
    boxes_in_goal = 0;
    for box in boxes:
        for goal in goals:
            if(box.y == goal.y and box.x == goal.x):
                boxes_in_goal += 1
                print("laatikko maalissa")
    if(boxes_in_goal == all_goals):
        print("Voitto!")
        return True
            
    
# Pääohjelma
def main():
    player_pos = [1, 1]  # Alusta pelaajan sijainti
    player = pygame.Rect(player_pos[0] * BLOCK_SIZE, player_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    kodarit = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
    kodarit_voitto = pygame.Rect(0, 0, BLOCK_SIZE * 12, BLOCK_SIZE * 8)
    print(player.right)
    create_and_draw_boxes()
    create_and_draw_goals()

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                #Tarkastetaan onko tapahtuma nuoli vasemmalle
                if event.key == pygame.K_LEFT:
                    key_pressed = "left"
                    #Ennen kuin pelihahmon sijaintia päivitetään, tarkistetaan,
                    #ettei kohdesolussa ole estettä
                    #(merkittynä numerolla 1). Tämä estää pelihahmoa liikkumasta
                    #seinien tai muiden esteiden läpi.
                    if MAP[player_pos[1]][player_pos[0] - 1] != 1:
                        #Vähennetään x positiota yhdellä
                        player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    key_pressed = "right"
                    if MAP[player_pos[1]][player_pos[0] + 1] != 1:
                        player_pos[0] += 1
                elif event.key == pygame.K_UP:
                    key_pressed = "up"
                    if MAP[player_pos[1] - 1][player_pos[0]] != 1:
                        player_pos[1] -= 1 
                elif event.key == pygame.K_DOWN:
                    key_pressed = "down"
                    if MAP[player_pos[1] + 1][player_pos[0]] != 1:
                        player_pos[1] += 1

                #Tehdään player rect uuteen positioon
                player = pygame.Rect(player_pos[0] * BLOCK_SIZE, player_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                
                #Tarkistetaan osuiko luntu laatikkoon ja riippuen mistä suunnasta lintu siihen osui siirretään laatikkoa
                for box in boxes:
                    if(pygame.Rect.colliderect(player, box.rect)):
                        if(key_pressed == "right"):
                            box.move(BLOCK_SIZE,0)
                        elif(key_pressed == "left"):
                            box.move(-BLOCK_SIZE,0)
                        elif(key_pressed == "down"):
                            box.move(0,BLOCK_SIZE)
                        elif(key_pressed == "up"):
                            box.move(0, -BLOCK_SIZE)

                            
                    #Tsekataan ovatko kaikki laatikot maaleissa ja jos niin näytetään voittoruutua
                    if(are_all_boxes_in_goals() == True):
                        screen.blit(kodarit_voitto_img, kodarit_voitto)
                        #Tämä käsky päivittää näytön
                        pygame.display.flip()
                        #Odotetaan 8 sekuntia, että näyttö päivittyy
                        pygame.time.wait(8000)
                        break
                                        

                    

        
        # Piiretään kenttä ja pelaaja
        screen.fill("#a6c6d5")
        draw_floor_and_walls()
        draw_goals()
        draw_boxes()
        screen.blit(player_img, player)
        screen.blit(kodarit_img, kodarit)
        #Tämä käsky päivittää näytön
        pygame.display.flip()
        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
