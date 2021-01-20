import g2d
from vehicle_frog import Frog, Vehicle
from raft import Raft
from actor import Arena
from river import River
from turtle import Turtle
from crocodile import Crocodile

game_start=False
level_start=False

frog_set=False

n_giocatori=1
level=1

arena_w=640
arena_h=480
arena = Arena(arena_w,arena_h)
river=River(arena)

rafts=[]
turtles=[]
vehicles=[]
crocodiles=[]

pos=0
type=0
raft_y=195
count=0
n_rafts=12
dim_rafts=1
rafts_row=0

for i in range(n_rafts):
    if count==4:
        if dim_rafts==3:
            dim_rafts=0
        dim_rafts+=1
        count=0
        rafts_row+=1
        if type==0:
            type=1
        else:
            type=0
        pos=0
        
        raft_y-=55
    rafts.append(Raft(arena, pos, raft_y, type, dim_rafts))
    pos+=220
    count+=1

pos=0
type=0
count=0
vehicle_y=402
n_vehicles=25
dim_vehicle=1

for i in range(n_vehicles):
    if count==5:
        dim_vehicle+=1
        count=0
        if type==0:
            type=1
        else:
            type=0
        pos=0
        vehicle_y-=31
    vehicles.append(Vehicle(arena, pos, vehicle_y, dim_vehicle))
    pos+=180
    count+=1
    
pos=0
speed=1
count=0
turtle_y=211
n_turtles=10
n_turtles_row=2

for i in range(n_turtles):
    if count==5:
        n_turtles_row+=1
        count=0
        if speed==2:
            speed=1
        else:
            speed=2
        pos=0
        pos+=50
        turtle_y-=51
    
    for c in range(n_turtles_row):
        turtles.append(Turtle(arena, (pos+(30*c)), turtle_y, speed))
    pos+=180
    count+=1
    
pos=0
crocodile_y=114
n_crocodiles=5
for i in range(n_crocodiles):
    crocodiles.append(Crocodile(arena, (pos+(180*i)), crocodile_y))

frog_1 = None
frog_2 = None

sprites = g2d.load_image("frogger_sprites.png")

river_img = g2d.load_image("frogger_bg.png")
logo = g2d.load_image("logo.png")

def update():
    global frog_1,frog_2,frog_set,level,level_start,game_start
    if game_start==False:
        g2d.fill_canvas((0,0,0))
        g2d.draw_image(logo,(60,60))
        g2d.draw_text_centered("v 1.0", (0,255,0), (624,475), 20)
        if n_giocatori==1:
            g2d.draw_text_centered("1 GIOCATORE", (255,0,0), (200,300), 30)
            g2d.draw_text_centered("2 GIOCATORI", (255,255,0), (410,300), 20)
        else:
            g2d.draw_text_centered("1 GIOCATORE", (255,255,0), (200,300), 20)
            g2d.draw_text_centered("2 GIOCATORI", (255,0,0), (410,300), 30)

        g2d.draw_text_centered("press ENTER to play", (255,255,255), (arena_w/2,400), 25)
    else:
        if level_start==False:
            g2d.fill_canvas((0,0,0))
            g2d.draw_text_centered("LEVEL", (255,0,0), (arena_w/2-25,arena_h/2), 70)
            g2d.draw_text_centered(str(level), (255,0,0), (arena_w/2+85,arena_h/2), 70)
            g2d.draw_text_centered("press ENTER to play", (255,255,255), (arena_w/2,400), 25)
        else:
            if n_giocatori==1:
                if frog_set==False:
                    frog_1 = Frog(arena, (arena_w/2)-20, arena_h-42)
                    frog_set=True
                if frog_1._dead==3:
                    g2d.fill_canvas((0,0,0))
                    g2d.draw_text_centered("GAME OVER", (255,0,0), (arena_w/2,arena_h/2), 70)
                elif frog_1._win==True:
                    frog_1.reset()
                    level_start=False
                    level+=1
                else:
                    frog_1.setcollideRaft()
                    frog_1.setcollideTurtle()
                    frog_1.setcollideRiver()
                    frog_1.setcollideCrocodile()
                    
                    arena.move_all()  # Game logic

                    background=g2d.load_image("frogger_bg.png")
                    g2d.draw_image(background,(0,0))
                    #g2d.fill_canvas((255,255,255))
                    
                    g2d.draw_text(("FROG 1 SCORE:"), (255, 0, 0), (0,0), 25)
                    g2d.draw_text((str(frog_1._score)), (255, 255, 0), (135,0), 25)
                    
                    g2d.draw_text(("LEVEL:"), (255, 0, 0), (550,0), 25)
                    g2d.draw_text((str(level)), (255, 255, 0), (615,0), 25)
                    
                    g2d.draw_text(("FROG 1 DEATHS:"), (255, 0, 0), (0,arena_h-16), 25)
                    deaths1=[]
                    for i in range(frog_1._dead):
                        deaths1.append('*')
                    g2d.draw_text((''.join(map(str, deaths1))), (255, 255, 0), (145,arena_h-16), 50)
                     
                    
                    for a in arena.actors():
                        if a!=river:
                            g2d.draw_image_clip(sprites, a.position(), a.symbol())
                        else:
                            g2d.draw_image_clip(river_img, a.position(), a.symbol())

                    if frog_1._y<=246:                        
                        frog_1.ctrl_win()
                        
                        for i in range(n_rafts):
                            if frog_1._y-3>=rafts[i]._y-5 and frog_1._y-3<=rafts[i]._y and (frog_1._x>=rafts[i]._x and frog_1._x<=rafts[i]._x+(rafts[i]._w-frog_1._w)):
                                if rafts[i]._type==0:
                                    frog_1._x-=rafts[i].getSpeed()
                                else:
                                    frog_1._x+=rafts[i].getSpeed()

                        for i in range(len(turtles)):
                            if frog_1._y-11==turtles[i]._y and (frog_1._x>=turtles[i]._x and frog_1._x<=turtles[i]._x+(turtles[i]._w-frog_1._w)):
                                frog_1._x-=turtles[i].getSpeed()
                                
                        for i in range(n_crocodiles):
                            if frog_1._y==crocodiles[i]._y and (frog_1._x>=crocodiles[i]._x and frog_1._x<=crocodiles[i]._x+(crocodiles[i]._w-frog_1._w)):
                                frog_1._x+=crocodiles[i].getSpeed()
                    
            else:
                if frog_set==False:
                    frog_1 = Frog(arena, (arena_w/4)-20, arena_h-42)
                    frog_2 = Frog(arena, ((arena_w/4)*3)-20, arena_h-42)
                    frog_set=True
                if frog_1._dead==3 or frog_2._dead==3 or frog_1._win==True or frog_2._win==True:
                    g2d.fill_canvas((0,0,0))
                    g2d.draw_text_centered("GAME OVER", (255,0,0), (arena_w/2,100), 70)
                    g2d.draw_text_centered("Classifica:", (255,255,0), (arena_w/2,150), 30)
                    if frog_1._score>frog_2._score:
                        g2d.draw_text_centered("1. Frog 1:", (255,255,0), (295,200), 30)
                        g2d.draw_text_centered((str(frog_1._score)), (255, 0, 0), (295+70,200), 30)
                        g2d.draw_text_centered("2. Frog 2:", (255,255,0), (295,250), 30)
                        g2d.draw_text_centered((str(frog_2._score)), (255, 0, 0), (295+70,250), 30)
                    elif frog_1._score<frog_2._score:
                        g2d.draw_text_centered("1.Frog 2:", (255,255,0), (295,200), 30)
                        g2d.draw_text_centered((str(frog_2._score)), (255, 0, 0), (295+70,200), 30)
                        g2d.draw_text_centered("2.Frog 1:", (255,255,0), (295,250), 30)
                        g2d.draw_text_centered((str(frog_1._score)), (255, 0, 0), (295+70,250), 30)
                    else:
                        g2d.draw_text_centered("Frog 1:", (255,255,0), (230,200), 30)
                        g2d.draw_text_centered((str(frog_1._score)), (255, 0, 0), (280,200), 30)
                        g2d.draw_text_centered("Frog 2:", (255,255,0), (380,200), 30)
                        g2d.draw_text_centered((str(frog_2._score)), (255, 0, 0), (430,200), 30)
                    
                elif frog_1._score<5000 and frog_2._score<5000:
                    
                    frog_1.setcollideRaft()
                    frog_1.setcollideTurtle()
                    frog_1.setcollideRiver()
                    frog_1.setcollideCrocodile()
                    
                    frog_2.setcollideRaft()
                    frog_2.setcollideTurtle()
                    frog_2.setcollideRiver()
                    frog_2.setcollideCrocodile()
                    
                    arena.move_all()  # Game logic
                    
                    background=g2d.load_image("frogger_bg.png")
                    g2d.draw_image(background,(0,0))
                    #g2d.fill_canvas((255,255,255))
                    
                    g2d.draw_text(("FROG 1 SCORE:"), (255, 0, 0), (0,0), 25)
                    g2d.draw_text((str(frog_1._score)), (255, 255, 0), (135,0), 25)
                    
                    g2d.draw_text(("FROG 2 SCORE:"), (255, 0, 0), (350,0), 25)
                    g2d.draw_text((str(frog_2._score)), (255, 255, 0), (485,0), 25)
                    
                    g2d.draw_text(("FROG 1 DEATHS:"), (255, 0, 0), (0,arena_h-16), 25)
                    deaths1=[]
                    for i in range(frog_1._dead):
                        deaths1.append('*')
                    g2d.draw_text((''.join(map(str, deaths1))), (255, 255, 0), (145,arena_h-16), 50)
                    
                    g2d.draw_text(("FROG 2 DEATHS:"), (255, 0, 0), (440,arena_h-16), 25)
                    deaths2=[]
                    for i in range(frog_2._dead):
                        deaths2.append('*')
                    g2d.draw_text((''.join(map(str, deaths2))), (255, 255, 0), (585,arena_h-16), 50)   
                    
                    for a in arena.actors():
                        if a!=river:
                            g2d.draw_image_clip(sprites, a.position(), a.symbol())
                        else:
                            g2d.draw_image_clip(river_img, a.position(), a.symbol())

                    if frog_1._y<=246:
                        if frog_1._bonus==False:
                            frog_1._score+=500
                            frog_1.setBonus()
                            
                        frog_1.ctrl_win()
                        
                        for i in range(n_rafts):
                            if frog_1._y-3>=rafts[i]._y-5 and frog_1._y-3<=rafts[i]._y and (frog_1._x>=rafts[i]._x and frog_1._x<=rafts[i]._x+(rafts[i]._w-frog_1._w)):
                                if rafts[i]._type==0:
                                    frog_1._x-=rafts[i].getSpeed()
                                else:
                                    frog_1._x+=rafts[i].getSpeed()
                        
                        for i in range(len(turtles)):
                            if frog_1._y-11==turtles[i]._y and (frog_1._x>=turtles[i]._x and frog_1._x<=turtles[i]._x+(turtles[i]._w-frog_1._w)):
                                frog_1._x-=turtles[i].getSpeed()
                                
                        for i in range(n_crocodiles):
                            if frog_1._y==crocodiles[i]._y and (frog_1._x>=crocodiles[i]._x and frog_1._x<=crocodiles[i]._x+(crocodiles[i]._w-frog_1._w)):
                                frog_1._x+=crocodiles[i].getSpeed()
                    
                    if frog_2._y<=246:
                        if frog_2._bonus==False:
                            frog_2._score+=500
                            frog_2.setBonus()
                        
                        frog_2.ctrl_win()

                        for i in range(n_rafts):
                            if frog_2._y-3>=rafts[i]._y-5 and frog_2._y-3<=rafts[i]._y and (frog_2._x>=rafts[i]._x and frog_2._x<=rafts[i]._x+(rafts[i]._w-frog_2._w)):
                                if rafts[i]._type==0:
                                    frog_2._x-=rafts[i].getSpeed()
                                else:
                                    frog_2._x+=rafts[i].getSpeed()
                        
                        for i in range(len(turtles)):
                            if frog_2._y-11==turtles[i]._y and (frog_2._x>=turtles[i]._x and frog_2._x<=turtles[i]._x+(turtles[i]._w-frog_2._w)):
                                frog_2._x-=turtles[i].getSpeed()
                            
                        for i in range(n_crocodiles):
                            if frog_2._y==crocodiles[i]._y and (frog_2._x>=crocodiles[i]._x and frog_2._x<=crocodiles[i]._x+(crocodiles[i]._w-frog_2._w)):
                                frog_2._x+=crocodiles[i].getSpeed()
                
def keydown(code):
    global game_start, n_giocatori,level_start
    if game_start==False:                
        if code == "ArrowLeft":
            n_giocatori=1
        if code == "ArrowRight":
            n_giocatori=2
        if code=="Return":
            game_start=True
            level_start=True
    elif game_start==True and level_start==False:
        if code=="Return":
            level_start=True
    else:
        if code == "ArrowUp":
            frog_1.go_up()
        elif code == "ArrowDown":
            frog_1.go_down()
        elif code == "ArrowLeft":
            frog_1.go_left()
        elif code == "ArrowRight":
            frog_1.go_right()
        
        if n_giocatori==2:
            if code == "KeyW":
                frog_2.go_up()
            elif code == "KeyS":
                frog_2.go_down()
            elif code == "KeyA":
                frog_2.go_left()
            elif code == "KeyD":
                frog_2.go_right()

def keyup(code):
    if game_start==True:
        frog_1.stay()
        if n_giocatori==2:
            frog_2.stay()

def main():
    g2d.init_canvas(arena.size())
    g2d.handle_keyboard(keydown, keyup)
    g2d.main_loop(update, 1000 // 30)
        
    
main()