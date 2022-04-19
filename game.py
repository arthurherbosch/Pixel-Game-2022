import pygame
from pygame.locals import *
from sklearn import tree

pygame.init()
clock = pygame.time.Clock()
fps = 60
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))  


pygame.display.set_caption('Drinkin Game')

background_img = pygame.image.load('img/map/BG.png')
bush_img = pygame.image.load('img/map/Objects/Bush (1).png')
wood_img= pygame.image.load('img/map/Objects/Bush (2).png')

tile_size = 50
def draw_grid():
    for line in range(0,24):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size),(screen_width, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size,0),(line * tile_size, screen_height))


class Player():
    def __init__(self, x,y):
        self.images_right = []
        self.images_left = []
      #  self.images_jump_right = []
      #  self.images_jump_left = []

        self.index = 0
       # self.index_jump = 0 
        self.counter = 0
       # self.counter_jump = 0
        
        for num in range(1,9):
            img_right = pygame.image.load(f'img/player1/walk/Run ({num}).png')
            img_right =  pygame.transform.scale(img_right, (50, 100))
            img_left =  pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        
        # for num in range(1,5):
        #     img_jump_right = pygame.image.load(f'img/player1/jump/Jump ({num}).png')
        #     img_jump_right =  pygame.transform.scale(img_jump_right, (100, 100))
        #     img_jump_left =  pygame.transform.flip(img_jump_right, True, False)
        #     self.images_jump_left.append(img_jump_left)
        #     self.images_jump_right.append(img_jump_right)

        
        
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y =  0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        
        walk_cooldown = 3
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -22
            self.jumped = True     
        if key[pygame.K_SPACE] == False:
         #   self.index_jump = 0
            self.jumped = False
        if key[pygame.K_LEFT]:
            self.direction = -1
            self.counter +=1
            dx -= 5
        if key[pygame.K_RIGHT]:
            self.direction = 1
            self.counter += 1
            dx += 5
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:    
                self.image = self.images_right[self.index]  
            if self.direction == -1:  
                self.image = self.images_left[self.index]  
  
      

        
        #handle animation walking
        if self.counter > walk_cooldown and self.jumped == False:
            self.counter = 1
            self.index += 1  
            if self.index >= len(self.images_right):
                self.index = 0 
            if self.direction == 1:    
                self.image = self.images_right[self.index]  
            if self.direction == -1:  
                self.image = self.images_left[self.index]  
  
        
       
        # add gravity
        self.vel_y += 2
        if self.vel_y > 10:
           self.vel_y = 10
        dy += self.vel_y

        # Collision
        
        for tile in world.title_list:
            # Check for collision in x-direction
            if tile[1].colliderect(self.rect.x + dx , self.rect.y, self.width, self.height):
                dx = 0
            # Check for collision in y-directoin
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                
                
    
    

        # update player coordinates            
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
            
        
        screen.blit(self.image, self.rect)
       # pygame.draw.rect(screen, (255,255,255), self.rect, 2)



class World():
    def __init__(self, data):
        self.title_list = []
        
        # SAND
        sand = pygame.image.load('img/map/Tile/5.png')
        sand_right = pygame.image.load('img/map/Tile/6.png')
        sand_left = pygame.image.load('img/map/Tile/4.png')
        sand_above = pygame.image.load('img/map/Tile/2.png')
        sand_bottom = pygame.image.load('img/map/Tile/9.png')
        sand_edge_right = pygame.image.load('img/map/Tile/3.png')
        sand_edge_left = pygame.image.load('img/map/Tile/1.png')
        sand_inner_left = pygame.image.load('img/map/Tile/8.png')
        sand_inner_right = pygame.image.load('img/map/Tile/10.png')
        sand_island = pygame.image.load('img/map/Tile/15.png')
        sand_island_left = pygame.image.load('img/map/Tile/14.png')
        sand_island_right= pygame.image.load('img/map/Tile/16.png')

        #BLOCKS
        stone_block = pygame.image.load('img/map/Objects/StoneBlock.png')
        cactus = pygame.image.load('img/map/Objects/Cactus (3).png')
        skeleton = pygame.image.load('img/map/Objects/Skeleton.png')

    
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(sand, (tile_size,tile_size))
                if tile == 2:
                    img = pygame.transform.scale(sand_right, (tile_size,tile_size))
                if tile == 3:
                    img = pygame.transform.scale(sand_above, (tile_size,tile_size))
                if tile == 4:
                    img = pygame.transform.scale(sand_bottom, (tile_size,tile_size))
                if tile == 5:
                    img = pygame.transform.scale(sand_left, (tile_size,tile_size))
                if tile == 6:
                    img = pygame.transform.scale(sand_edge_right, (tile_size,tile_size))
                if tile == 7:
                    img = pygame.transform.scale(sand_edge_left, (tile_size,tile_size))
                if tile == 8:
                    img = pygame.transform.scale(sand_inner_left, (tile_size,tile_size))
                if tile == 9:
                    img = pygame.transform.scale(sand_inner_right, (tile_size,tile_size))
                if tile == 10:
                    img = pygame.transform.scale(cactus, (tile_size,tile_size))
                if tile == 11:
                    img = pygame.transform.scale(sand_island, (tile_size,tile_size))
                if tile == 12:
                    img = pygame.transform.scale(sand_island_left, (tile_size,tile_size))
                if tile == 13:
                        img = pygame.transform.scale(sand_island_right, (tile_size,tile_size))
                if tile == 14:
                    img = pygame.transform.scale(skeleton, (tile_size * 3,tile_size))
            
                if tile != 0:
                    img_rect = img.get_rect()
                    img_rect.x = (col_count * tile_size)
                    img_rect.y = (row_count * tile_size)
                    title = (img, img_rect)
                    self.title_list.append(title)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.title_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255,255,255), tile[1], 2 )
                    

world_data = [
 [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5], 
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
    [9,6,0,0,0,0,0,12,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
    [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,13,0,0,0,0,0,5],
    [1,9,3,3,13,0,0,0,0,0,0,12,11,13,0,0,0,0,0,0,0,0,0,5],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,5], 
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,3,6,0,0,0,0,5],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1,2,0,0,0,0,5], 
    [2,0,0,0,0,0,0,0,7,3,6,0,0,0,3,0,5,1,2,10,14,0,0,5],
    [9,3,3,3,3,6,0,0,5,1,2,0,0,0,0,0,5,1,9,3,3,3,3,8],
    [1,1,1,1,1,2,10,10,5,1,2,10,10,10,10,10,5,1,1,1,1,1,1,1]
    
    
]
player = Player(50, screen_height)
world = World(world_data)

run = True
while run:
    
    clock.tick(fps)
    screen.blit(background_img, (0,0))
    screen.blit(bush_img, (550,120))
    screen.blit(wood_img,(100,430))
    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run.false
            
    pygame.display.update()
    
pygame.quit()

            
    