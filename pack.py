import pygame
import sys
import os
import random
from PIL import Image

pygame.init()
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("thiscord")
clock = pygame.time.Clock()

fnt = pygame.font.SysFont("Arial", 22)
fnt_b = pygame.font.SysFont("Arial", 20, bold=True)

bp = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")

frames = []
try:
    img = Image.open(os.path.normpath(os.path.join(bp, "assets/ttc.gif")))
    for i in range(img.n_frames):
        img.seek(i)
        rgba = img.convert("RGBA")
        pg_img = pygame.image.fromstring(rgba.tobytes("raw", "RGBA"), rgba.size, "RGBA")
        frames.append(pygame.transform.scale(pg_img, (200, 200)))
except Exception as e:
    print("NOT OK! GIF", e)
    s = pygame.Surface((200, 200))
    s.fill((200, 50, 50))
    frames.append(s)

roasts = [
    "garden gnome", "chicken bone", "google chrome",
    "no home", "student loan", "underground flintstone",
    "ice cream cone"
]

chat = [{"user": "jay435", "color": (200, 50, 50), "msg": "my dog died", "gif": False}]

msg = ""
started = False
sent = False
f_idx = 0
f_tick = 0

cy = 0 
tx = 0 
dragging = False

spam_btn = pygame.Rect(20, 520, 150, 50)
send_btn = pygame.Rect(180, 520, 120, 50)
scroll_bg = pygame.Rect(25, 480, 750, 10)

def draw_chat(surf, m, start_y, cur_f):
    surf.blit(fnt_b.render(m["user"], True, m["color"]), (20, start_y))
    y = start_y + 25
    
    if m["gif"]:
        surf.blit(frames[cur_f], (20, y))
        return y + 210
        
    line = ""
    for w in m["msg"].split(" "):
        if fnt.size(line + w)[0] < 740:
            line += w + " "
        else:
            surf.blit(fnt.render(line, True, (220, 220, 220)), (20, y))
            y += 25
            line = w + " "
            
    surf.blit(fnt.render(line, True, (220, 220, 220)), (20, y))
    return y + 35

while True:
    tw = fnt.size(msg)[0]
    max_tx = max(0, tw - 740)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if e.type == pygame.MOUSEWHEEL:
            cy += e.y * 30
            
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if scroll_bg.collidepoint(e.pos) and not sent:
                dragging = True
                
            if spam_btn.collidepoint(e.pos) and not sent:
                if not started:
                    msg = "shut yo "
                    started = True
                else:
                    msg += random.choice(roasts) + " "
                
                tx = max(0, fnt.size(msg)[0] - 740)
                    
            if send_btn.collidepoint(e.pos) and started and not sent:
                msg += "ASS UP" if random.randint(1, 100) == 1 else "BUTT UP 🤣🤣 ROASTED BOII"
                #1 perccent chacne of having "ASS UP" instead "BUTT UP" btw
                
                chat.append({"user": "You", "color": (50, 200, 50), "msg": msg, "gif": False})
                chat.append({"user": "jay435", "color": (200, 50, 50), "msg": "", "gif": True})
                
                msg = ""
                tx = 0
                sent = True
                cy = -9999 
                
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            dragging = False
            
        if e.type == pygame.MOUSEMOTION and dragging and max_tx > 0:
            mx = max(25, min(e.pos[0], 775))
            tx = ((mx - 25) / 750) * max_tx

    tx = max(0, min(tx, max_tx))
    
    total_y = 20
    for c in chat:
        if c["gif"]:
            total_y += 235
            continue
            
        l = ""
        for w in c["msg"].split(" "):
            if fnt.size(l + w)[0] >= 740:
                total_y += 25
                l = w + " "
            else:
                l += w + " "
        total_y += 60
            
    max_cy = max(0, total_y - 410)
    cy = max(-max_cy, min(cy, 0))

    f_tick += 1
    if f_tick > 3:
        f_idx = (f_idx + 1) % len(frames)
        f_tick = 0

    win.fill((44, 47, 51))
    
    win.set_clip(pygame.Rect(0, 0, 800, 410))
    cur_y = 20 + cy
    for c in chat:
        cur_y = draw_chat(win, c, cur_y, f_idx)
    win.set_clip(None)
        
    pygame.draw.line(win, (35, 39, 42), (0, 420), (800, 420), 2)
    
    if not sent:
        pygame.draw.rect(win, (60, 64, 70), (20, 440, 760, 60), border_radius=5)
        
        win.set_clip(pygame.Rect(25, 445, 750, 30))
        win.blit(fnt.render(msg, True, (200, 200, 200)), (30 - tx, 448))
        win.set_clip(None)
        
        pygame.draw.rect(win, (40, 43, 48), scroll_bg, border_radius=3)
        if max_tx > 0:
            thumb_w = max(30, (740 / tw) * 750)
            thumb_x = 25 + (tx / max_tx) * (750 - thumb_w)
            pygame.draw.rect(win, (100, 105, 115), (thumb_x, 480, thumb_w, 10), border_radius=3)
    
    pygame.draw.rect(win, (88, 101, 242), spam_btn, border_radius=5)
    win.blit(fnt_b.render("Roast", True, (255, 255, 255)), (spam_btn.x + 15, spam_btn.y + 12))
    
    c_btn = (88, 101, 242) if started and not sent else (100, 100, 100)
    pygame.draw.rect(win, c_btn, send_btn, border_radius=5)
    win.blit(fnt_b.render("Finalize", True, (255, 255, 255)), (send_btn.x + 25, send_btn.y + 12))
    
    pygame.display.flip()
    clock.tick(60)

    # kipWasHere
    # 17/7/2026 1:01 PM UTC+8