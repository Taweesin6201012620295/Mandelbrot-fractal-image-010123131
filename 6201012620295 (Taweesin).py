import threading
import time
import pygame

print( 'File:', __file__ )
# function of mandelbrot solution
def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z**4 + c
        i += 1 
    return i
# Take mandelbrot by threading
def Th_mandelbrot(surface,TH_1,Lock,sem):
    scale = 0.006
    offset = complex(0,0.0)
    if sem.acquire(timeout=0.1):
        for x in range(TH_1*Screen_N,(TH_1+1)*Screen_N):
            for y in range(scr_h):
                with Lock:
                    re = scale*(x-w2) + offset.real
                    im = scale*(y-h2) + offset.imag
                    c = complex( re, im )
                    color = mandelbrot(c, 63)
                    r = (color << 6) & 0xc0
                    g = (color << 4) & 0xc0
                    b = (color << 2) & 0xc0
                    surface.set_at( (x, y), (255-r,255-g,255-b) )

# initialize pygame
pygame.init()

# create a screen of width=700 and height=600
scr_w, scr_h = 700, 600
screen = pygame.display.set_mode( (scr_w, scr_h) )

# set window caption
pygame.display.set_caption('Fractal Image: Mandelbrot') 

# create a clock
clock = pygame.time.Clock()

# create a surface for drawing
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

# create a thread lock 
Lock = threading.Lock()

# set the number of threads to be created
N = 10

Screen_N = int(scr_w/N)
# create a list of semaphores 
list_sem = [ threading.Semaphore(0) for i in range(N) ]
# a list for keeping the thread objects
list_threads = []

running = True
w2, h2 = scr_w/2, scr_h/2 # half width, half screen
# a list for keeping the thread objects
for i in range(N):
    sem = list_sem[i]
    t = threading.Thread(target=Th_mandelbrot, args=(surface,i,Lock,sem))
    list_threads.append( t ) 

# start threads
for t in list_threads:
    t.start()

while running:

    for sem in list_sem:
        sem.release()

    # draw the surface on the screen
    screen.blit( surface, (0,0) )
    # update the display
    pygame.display.update()

    clock.tick(110) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
print( 'PyGame done...')