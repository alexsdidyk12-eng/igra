from ursina import*

app = Ursina()

#camera
camera.orthographic = True
camera.fov=39
window.color=color.rgb(100,180,255)
bg1 = Entity(model="quad", texture=None, color=color.rgb(150,200,255),
             scale=(50,20,1), z=1)
bg2 = Entity(model="quad", texture=None, color=color.rgb(120,170,240),
             scale=(70,25,1), z=2)


#sounds
jump_sound=Audio("assets/jump.wav", autoplay=False)
coin_sound=Audio("assets/coin.wav", autoplay=False)


#player
player=Entity(
    model="cube",
    color=color.orange,
    scale=(1,1.5,1),
    collider="box",
    position=(5,15,15) #x,y,z
)
#speed
player.y_velocity=0
GRAVITY=-20
JUMP_FORCE=12
MOVE_SPEED=5

#platforms
platforms=[]

def add_platform(x,y,width=4, height=1):
    p = Entity(
        model="cube",
        color=color.green,
        scale=(width,height,1),
        position=(x,y,0),
        collider="box")
    platforms.append(p)

# ground
add_platform(0,-3,width=12, height=1)
add_platform(3,5,width=3)
add_platform(-4,0,width=3)
add_platform(9,4,width=4)
add_platform(14,0,width=3)
add_platform(11,18,width=3)
add_platform(16,9,width=4)
add_platform(19,11,width=3)
add_platform(23,14,width=3)
add_platform(20,16,width=5)
add_platform(28,18,width=3)
add_platform(7,11,width=3)
add_platform(-6,15,width=3)
add_platform(3,13,width=3)
add_platform(6,9,width=3)
add_platform(12,11,width=3)
#moving platform
def add_moving_platform(x,y,width, height=1, speed=2, min_x=-5,max_x=5):
    p = Entity(
        model="cube",
        color=color.azure,
        scale=(width,height,1),
        position=(x,y,0),
        collider="box")
    p.speed=speed
    p.min_x=min_x
    p.max_x=max_x
    p.direction=1
    platforms.append(p)
    return p

moving_platform=add_moving_platform(12,2,width=4,min_x=10,max_x=16)




def is_on_ground():
    player.y-=0.05
    hit_info=player.intersects()
    player.y+=0.05
    
    if hit_info.hit:
        player.y = hit_info.entity.world_y + (hit_info.entity.scale_y / 2)+(player.scale_y /2)
        return True
    return False

score =0
score_text=Text(f"Score: {score}", x=-0.85, y=0.45, scale=1.2,color=color.black)
coins= []

def add_coin(x,y):
    coin = Entity(model="sphere", color=color.yellow, scale=0.5, position=(x,y,0), collider="box")
    coins.append(coin)
    
add_coin(3,6)
add_coin(16,9.5)
add_coin(14,1)
add_coin(28,19)
add_coin(11,19)
add_coin(-6,16)
add_coin(20,17)
add_coin(23,15)
#enemy

enemy=Entity(
    model="cube",
    color=color.red,
    scale=(1,1,1),
    position=(-12,1,0),
    collider="box"
)
enemy.direction=1
#finish
finish=Entity(
    model="cube",
    color=color.lime,
    scale=(1,3,1),
    position=(20,1,0),
    collider="box"
)

#lives
lives=3
lives_text=Text(f"Lives: {lives}", x=-0.85, y=0.35, scale=1.2, color=color.black)

#timer
level_time=0
time_text=Text("Time:0", x=0.6, y=0.45, scale=1.2, color=color.black)
def update():
    bg1.x=camera.x*0.5
    bg2.x=camera.x*0.25
    global score, lives, level_time
    move_x=0
    if held_keys["a"] or held_keys["left arrow"]:
        move_x -= MOVE_SPEED * time.dt 
    if held_keys["d"] or held_keys["left arrow"]:
        move_x += MOVE_SPEED * time.dt 
        
    player.x += move_x
    #jump     
    if(held_keys["space"] or held_keys["w"] or held_keys["up arrow"]) and is_on_ground():
        jump_sound.play()
        player.y_velocity = JUMP_FORCE
    
    #gravity
    player.y_velocity+=GRAVITY* time.dt 
    player.y += player.y_velocity * time.dt
    
    if is_on_ground():
        player.y_velocity=0
    
    camera.x = lerp(camera.x, player.x, 5 * time.dt)
    
    if player.y < -10:
        player.position = (0,1,0)
        player.y_velocity = 0
        
        
    #coin animation
    for coin in coins:
        if coin.enabled:
            coin.rotation_y += 120 * time.dt 
    #coin collection
    for coin in coins:
        if coin.enabled and player.intersects(coin).hit:
            coin_sound.play()
            coin.disable()
            score+=1
            score_text.text=f"Score: {score}"
    #enemy
    enemy.x += enemy.direction *2 * time.dt
    
    if enemy.x>15:
        enemy.direction=-1
        
    if enemy.x<-12:
        enemy.direction=1
     # enemy kill / damage logic
    hit = player.intersects(enemy)

    if hit.hit and enemy.enabled:
        # kill enemy — удар сверху
        if player.y > enemy.y + 0.5:
            enemy.disable()
            player.y_velocity = 8
            score += 1
            score_text.text = f"Score: {score}"
        else:
             # player takes damage
            lives -=1
            lives_text.text = f"Lives: {lives}"
            player.position = (0, 1, 0)
            player.y_velocity = 0
    
           
      
    
    #kill enemy
    
    if player.intersects(enemy).hit:
        if player.y > enemy.y + 0.5:
            enemy.disable()
            player.y_velocity=8
            score+=1
            score_text.text=f"Score: {score}"
    #level time
    level_time += time.dt
    time_text.text =f"Time: {int(level_time)}"
    #moving platforms
    for p in platforms:
        if hasattr(p,"min_x"):
            p.x+=p.direction*p.speed*time.dt
            if p.x>p.max_x:
                p.direction=-1
            if p.x<p.min_x:
                p.direction=1
    #finish
    if player.intersects(finish).hit:
        Text("YOU WIN!", origin=(0,0), scale=3, color=color.black)
        application.paused=True
Text(
    "A/D or <-/-> for walking n/space for jump collect all coins to win",
    origin=(-0.9,0.9),
    scale=0.7,
    color=color.black
)

app.run()