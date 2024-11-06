import pygame, random, copy
import nltk
nltk.download('words')

pygame.init()

wordlist = []
from nltk.corpus import words
wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key = len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))
print(len_indexes)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typing Game')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

#GAME
level = 1
new_level = True
active_string = ''
score = 0
lives = 3
paused = True
submit = ''
words = []
choices = [False, False, False, True, False, False, False]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#LOAD ASSETS FONTS AND SOUND AFFECTS
header_font = pygame.font.Font('assets/fonts/square.ttf', 50)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 38)
banner_font = pygame.font.Font('assets/fonts/openSans.ttf', 28)
font = pygame.font.Font('assets/fonts/openSans.ttf', 48)
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('assets/sounds/woosh.mp3')
wrong = pygame.mixer.Sound('assets/sounds/wrong.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

class Word:
    def __init__(self, text, speed, y, x):
        self.text = text
        self.speed = speed
        self.y = y
        self.x = x
    def draw(self):
        color = 'black'
        screen.blit(font.render(self.text, True, color), (self.x, self.y))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x, self.y))
    def update(self):
        self.x -= self.speed
class Button:
    def __init__(self, x, y, text, clicked, surf):
        self.x = x
        self.y = y
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        circ = pygame.draw.circle(self.surf, (45, 89, 135), (self.x, self.y), 35)
        if circ.collidepoint(pygame.mouse.get_pos()):
            btns = pygame.mouse.get_pressed()
            if btns[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x, self.y), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf,(190, 89, 135), (self.x, self.y), 35)
        pygame.draw.circle(self.surf, 'white', (self.x, self.y), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x - 15, self.y - 25))

def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100])
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    #LEVEL, PLAYER INPUT, HIGH SCORE, SCORE, LIVES, PAUSE
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 75))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 75))
    pause_btn = Button(748, HEIGHT - 50, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (250, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'white'), (550, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'white'), (10, 10))
    return pause_btn.clicked
def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 200, '|>', False, surface)
    resume_btn.draw()
    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()

    surface.blit(header_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(header_font.render('PLAY', True, 'white'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'white'), (450, 175))
    surface.blit(header_font.render('Active Letter Lengths: ', True, 'white'), (110, 250))

    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked
def check_answer(sc):
    for wr in word_objs:
        if wr.text == submit:
            points = wr.speed * len(wr.text) * 10 * (len(wr.text) / 3)
            sc += int(points)
            word_objs.remove(wr)
            woosh.play()
    return sc
def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))
    for i in range(level):
        speed = random.randint(2, 3)
        y = random.randint(10 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y, x)
        word_objs.append(new_word)

    return word_objs
def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

word_objs = []
run = True
while run:
    screen.fill('gray')
    timer.tick(fps)
    #BACKGROUND - STATUSES - BUTTON STATUS
    pause_bt = draw_screen()
    if paused:
        resume_bt, changes, quit_bt = draw_pause()
        if resume_bt:
            paused = False
        if quit_bt:
            check_high_score()
            run = False
    elif new_level and not paused:
        word_objs = generate_level()
        new_level = False
    else:
        for w in word_objs:
            w.draw()
            if not paused:
                w.update()
            if w.x < -200:
                word_objs.remove(w)
                lives -= 1
    if len(word_objs) <= 0 and not paused:
        level += 1
        new_level = True
    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                    click.play()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes
    if pause_bt:
        paused = True
    if lives <= 0:
        paused = True
        level = 1
        lives = 3
        word_objs = []
        new_level = True
        check_high_score()
        score = 0
    pygame.display.flip()
pygame.quit()