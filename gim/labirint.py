from pygame import*
window = display.set_mode((500, 500))
BLACK = (0,0,0)
WHITE= (255, 255, 255)
display.set_caption('Labirin')
bakcground=image.load('bg.jpg')
bakcground=transform.scale(bakcground,(500, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, image_file, height, width, x, y):
        super().__init__()
        self.image = image.load(image_file) 
        self.image = transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect() 
								    
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def __init__(self, image_file, height, width, x, y,speed_x,speed_y):
        super().__init__(image_file, height, width, x, y)
        self.speed_x = speed_x
        self.speed_y= speed_y
    def update(self):
        self.rect.x += self.speed_x
        platform_touched= sprite.spritecollide(self,barriers,False)
        if self.speed_x > 0 :
            for p in platform_touched:
                self.rect.right= min(self.rect.right,p.rect.left)
        elif self.speed_x < 0 :
            for p in platform_touched:
                self.rect.left= max(self.rect.left,p.rect.right)
                
        self.rect.y += self.speed_y
        platform_touched= sprite.spritecollide(self,barriers,False)
        if self.speed_y > 0 :
            for p in platform_touched:
                self.rect.bottom= min(self.rect.bottom,p.rect.top)
        elif self.speed_y < 0 :
            for p in platform_touched:
                self.rect.top= max(self.rect.top,p.rect.bottom)
    def fire(self):
        bullet=Bullet('pluru.png',30,10,self.rect.right,self.rect.centery,20)
        group_bullet.add(bullet)



class Enemy (GameSprite):
    def __init__(self, image_file, height, width, x, y,x_awal,x_akhir,speed):
        super().__init__(image_file, height, width, x, y)
        self.x_awal= x_awal
        self.x_akhir=x_akhir
        self.speed=speed
    def update_pos(self):
        self.rect.x += self.speed 
        if self.rect.x < self.x_awal and self.speed < 0 :
            self.speed *= -1
        if self.rect.x > self.x_akhir and self.speed > 0 :
            self.speed *= -1
class Bullet (GameSprite):
    def __init__(self, image_file, height, width, x, y,speed):
        super().__init__(image_file, height, width, x, y)
        self.speed=speed
    def apdet(self):
        self.rect.x += self.speed
        if self.rect.x > 500:
            self.kill()

class Wall (GameSprite):
    def __init__(self, image_file, height, width, x, y):
        super().__init__(image_file, height, width, x, y)
class Finish (GameSprite):
    def __init__(self, image_file, height, width, x, y):
        super().__init__(image_file, height, width, x, y)
finish = Finish('finish.jpeg', 50, 50, 450, 450)
player= Player('peu.png',90,90,0,0,0,0)
enemy= Enemy('pou.png',90,90,330,330,10,500,5)
enemy1= Enemy('pou.png',90,90,330,0,0,10,5)
dinding= Wall('dinding.jpeg',650,50,350,-300)
dinding1= Wall ('dinding.jpeg',150,50,200,350)
font.init()
font=font.SysFont('Arial',100)
pesan_menang = font.render ('Anda Menang',True,WHITE)
pesan_kalah = font.render ('Anda Kalah',True,BLACK)
barriers = sprite.Group()
barriers.add(dinding)
barriers.add(dinding1)
group_bullet=sprite.Group()
group_enemy= sprite.Group()
group_enemy.add(enemy)
group_enemy.add(enemy1)
done= False
run = True
while run:
    if done == False:
        time.delay(50)
        window.blit(bakcground,(0,0))
        player.reset()
        group_enemy.draw(window)
        finish.reset()
        player.update() 
        barriers.draw(window)
        group_bullet.draw(window)
        for bullet in group_bullet:
            bullet.apdet() 
        sprite.groupcollide(group_bullet, barriers, True, False)
        sprite.groupcollide(group_bullet, group_enemy, True, True)
        for enemy in group_enemy:
            enemy.update_pos()  
    if sprite.collide_rect(player,finish):
        window.blit (pesan_menang,(50,50))
        done= True
    if sprite.spritecollide(player,group_enemy,False):
        window.blit(pesan_kalah,(50,50))
        done = True


   
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_a and player.rect.x >0 :
                player.speed_x= -5
            if e.key == K_d and player.rect.x < 500 - 90 :
                player.speed_x= 5
            if e.key == K_w and player.rect.y > 0 :
                player.speed_y= -5
            if e.key == K_s:
                player.speed_y= 5
        if e.type == KEYUP:
            if e.key == K_a and player.rect.x  >0 :
                player.speed_x=0
            if e.key == K_d:
                player.speed_x= 0
            if e.key == K_w:
                player.speed_y= 0
            if e.key == K_s:
                player.speed_y= 0
            if e.key == K_f:
                player.fire()
            


    display.update()



