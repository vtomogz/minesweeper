import pygame
import random
import datetime

rows = 16
cols = 30

field_size = 40
bar_size = field_size*2

nr_bombs = 99
to_reveal = rows * cols - nr_bombs
bombs_counter = nr_bombs

started = False
lost = False
won = False

pygame.init()
font = pygame.font.SysFont(None,int(field_size*1.5))

class Endscreen(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([int(field_size*cols/2),int((field_size*rows+bar_size)/2)])
		self.image.fill((0,0,0))
		pygame.draw.rect(self.image, (128, 128, 128),[5,5,int(field_size*cols/2-10),int((field_size*rows+bar_size)/2-10)])
		self.rect = self.image.get_rect()
		self.font = pygame.font.SysFont(None,int(bar_size*0.7))

	def draw(self,screen,elapsed_time):
		screen.blit(self.image,(int((screen.get_width()-self.rect.width)/2),int((screen.get_height()-self.rect.height)/2)))
		if lost:
			self.text1 = self.font.render("You lost.",True,(0,0,0))
			self.text2 = self.font.render("Press Enter to try again.",True,(0,0,0))
			self.text3 = self.font.render("Press Esc to exit.",True,(0,0,0))
			screen.blit(self.text2,(int((screen.get_width()-self.text2.get_width())/2),int((screen.get_height()-self.text2.get_height())/2)))
			screen.blit(self.text1,(int((screen.get_width()-self.text1.get_width())/2),int((screen.get_height()-self.text1.get_height())/2-self.text2.get_height())))
			screen.blit(self.text3,(int((screen.get_width()-self.text3.get_width())/2),int((screen.get_height()-self.text3.get_height())/2+self.text2.get_height())))
		if won:
			self.text1 = self.font.render("You won in "+"{:02}:{:02}.".format(int(elapsed_time.seconds/60),elapsed_time.seconds%60),True,(0,0,0))
			self.text2 = self.font.render("Press Enter to try again.",True,(0,0,0))
			self.text3 = self.font.render("Press Esc to exit.",True,(0,0,0))
			screen.blit(self.text2,(int((screen.get_width()-self.text2.get_width())/2),int((screen.get_height()-self.text2.get_height())/2)))
			screen.blit(self.text1,(int((screen.get_width()-self.text1.get_width())/2),int((screen.get_height()-self.text1.get_height())/2-self.text2.get_height())))
			screen.blit(self.text3,(int((screen.get_width()-self.text3.get_width())/2),int((screen.get_height()-self.text3.get_height())/2+self.text2.get_height())))




class InformationBar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([field_size * cols, bar_size])
		self.image.fill((0,0,0))
		pygame.draw.rect(self.image, (128, 128, 128),[1,1,field_size*cols-2,bar_size-2])
		self.rect = self.image.get_rect()
		self.bar_font = pygame.font.SysFont(None,int(bar_size*1.1))
		self.bombs_text = self.bar_font.render(str(bombs_counter), True, (0,0,0))
		self.timer_text = self.bar_font.render("00:00", True, (0,0,0))

	def draw(self, screen):
		screen.blit(self.image,self.rect)
		screen.blit(self.bombs_text,(int((self.rect.width-self.bombs_text.get_width())/15),int((self.rect.height-self.bombs_text.get_height())/2)))
		screen.blit(self.timer_text,(int((self.rect.width-self.timer_text.get_width())/2),int((self.rect.height-self.timer_text.get_height())/2)))

	def update(self, bombs,elapsed_time):
		self.bombs_text = self.bar_font.render(str(bombs), True, (0,0,0))
		self.timer_text = self.bar_font.render("{:02}:{:02}".format(int(elapsed_time.seconds/60),elapsed_time.seconds%60), True, (0,0,0))


class Field(pygame.sprite.Sprite):
	def __init__(self, value):
		super().__init__()

		self.value = int(value)
		self.image = pygame.Surface([field_size, field_size])
		self.image.fill((0,0,0))
		pygame.draw.rect(self.image, (128, 128, 128),[1,1,field_size-2,field_size-2])
		self.rect = self.image.get_rect()

		self.revealed = pygame.Surface([field_size,field_size])
		self.revealed.fill((0,0,0))
		pygame.draw.rect(self.revealed, (70,70,70), [1,1,field_size-2,field_size-2])
		if self.value > 0:
			self.text = font.render(value, True, (255,255,255))
			self.revealed.blit(self.text,(int((self.rect.width-self.text.get_width())/2),int((self.rect.height-self.text.get_height())/2)))
		self.is_revealed = False
		if self.value==-1:
			pygame.draw.circle(self.revealed,(0,0,0),[int(field_size/2),int(field_size/2)],int(field_size/2*0.7))

		self.locked = pygame.Surface([field_size,field_size])
		self.locked.fill((0,0,0))
		pygame.draw.rect(self.locked,(128, 128, 128),[1,1,field_size-2,field_size-2])
		pygame.draw.circle(self.locked,(255,0,0),[int(field_size/2),int(field_size/2)],int(field_size/2*0.7))
		self.is_locked = False

		self.unrevealed = pygame.Surface([field_size, field_size])
		self.unrevealed.fill((0,0,0))
		pygame.draw.rect(self.unrevealed, (128, 128, 128),[1,1,field_size-2,field_size-2])

		self.highlighted = pygame.Surface([field_size, field_size])
		self.highlighted.fill((0,0,0))
		pygame.draw.rect(self.highlighted, (200, 200, 200),[1,1,field_size-2,field_size-2])

	def lock(self):
		global bombs_counter
		if not self.is_revealed:
			if self.is_locked:
				self.image = self.unrevealed
				self.is_locked = False
				bombs_counter = bombs_counter + 1
			else:
				self.image = self.locked
				self.is_locked = True
				bombs_counter = bombs_counter - 1

	def reveal(self):
		if not self.is_locked and not self.is_revealed:
			self.is_revealed = True
			self.image = self.revealed
			global started
			started = True
			global lost
			if self.value==-1:
				lost=True
			global to_reveal
			to_reveal -= 1
		return

	def highlight(self, switch):
		if switch and not self.is_revealed and not self.is_locked:
			self.image = self.highlighted
		elif not switch and not self.is_revealed and not self.is_locked:
			self.image = self.unrevealed
		return

def count_marked(fields, x, y):
	vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	counter = 0
	for vector in vectors:
		if 0 <= x+vector[0] < rows and 0 <= y+vector[1] < cols:
			if fields[(x+vector[0])*cols+y+vector[1]].is_locked:
				counter += 1
	return counter

def count_bombs(matrix, x, y):
	vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	counter = 0
	for vector in vectors:
		if 0 <= x+vector[0] < rows and 0 <= y+vector[1] < cols:
			if matrix[x+vector[0]][y+vector[1]] == -1:
				counter += 1
	return counter

def reveal(fields, x, y):
	vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	fields[x*cols+y].reveal()
	if fields[x*cols+y].value == 0:
		for vector in vectors:
			if 0 <= x+vector[0] < rows and 0 <= y+vector[1] < cols:
				if not fields[(x+vector[0])*cols+y+vector[1]].is_revealed:
					reveal(fields, x+vector[0],y+vector[1])
	return


def coords(mouseposition):
	x = mouseposition[0] / field_size
	y = (mouseposition[1] - bar_size )/ field_size
	return [int(x),int(y)]


def main():
	want_to_play = True
	global lost
	global won
	global started
	global bombs_counter
	global to_reveal


	window = pygame.display.set_mode((cols*field_size,rows*field_size+bar_size))

	while(want_to_play):
		started = False
		bombs_counter=nr_bombs
		to_reveal = cols*rows-nr_bombs

		bar = InformationBar()

		end = Endscreen()

		seed = []
		for i in range(rows*cols):
			if i < nr_bombs:
				seed.append(-1)
			else:
				seed.append(0)
		random.shuffle(seed)

		game_field = []
		for i in range(rows):
			game_field.append([])
			for j in range(cols):
				game_field[i].append(seed[i*cols+j])
		for i in range(rows):
			for j in range(cols):
				if game_field[i][j] != -1:
					game_field[i][j] = count_bombs(game_field, i, j)

		field_list = pygame.sprite.Group()
		for i in range(rows):
			for j in range(cols):
				field = Field(str(game_field[i][j]))
				field.rect.x = j * field_size
				field.rect.y = i * field_size + bar_size
				field_list.add(field)

		elapsed_time = datetime.timedelta(0)

		GameLoop = True
		double_pressed=False

		while GameLoop:
			if to_reveal < 1:
				won = True
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if lost or won:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							want_to_play = False
							GameLoop = False
							break
						if event.key == pygame.K_RETURN:
							lost = False
							won = False
							GameLoop = False
							break
				if not lost and not won:
					if pygame.mouse.get_pos()[1]>bar_size:
						if event.type == pygame.MOUSEMOTION:
							try:
								field_list.sprites()[mousepos[1]*cols+mousepos[0]].highlight(False)
							except:
								pass
							mousepos = coords(pygame.mouse.get_pos())
							field_list.sprites()[(mousepos[1])*cols+mousepos[0]].highlight(True)

						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							mousepos = coords(pygame.mouse.get_pos())
							reveal(field_list.sprites(),mousepos[1],mousepos[0])

						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
							mousepos = coords(pygame.mouse.get_pos())
							field_list.sprites()[mousepos[1]*cols+mousepos[0]].lock()


						if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[2]:
							mousepos = coords(pygame.mouse.get_pos())
							if field_list.sprites()[mousepos[1]*cols+mousepos[0]].is_revealed:
								if field_list.sprites()[mousepos[1]*cols+mousepos[0]].value == count_marked(field_list.sprites(),mousepos[1],mousepos[0]):
									vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
									for vector in vectors:
										if 0 <= mousepos[1]+vector[0] < rows and 0 <= mousepos[0]+vector[1] < cols:
											reveal(field_list.sprites(),mousepos[1]+vector[0],mousepos[0]+vector[1])
								else:
									double_pressed=True
									vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
									for vector in vectors:
										if 0 <= mousepos[1]+vector[0] < rows and 0 <= mousepos[0]+vector[1] < cols:
											field_list.sprites()[(mousepos[1]+vector[0])*cols+mousepos[0]+vector[1]].highlight(True)

						if double_pressed:
							if not pygame.mouse.get_pressed()[0] or not pygame.mouse.get_pressed()[2]:
								mousepos = coords(pygame.mouse.get_pos())
								double_pressed=False
								vectors = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
								for vector in vectors:
									if 0 <= mousepos[1]+vector[0] < rows and 0 <= mousepos[0]+vector[1] < cols:
										field_list.sprites()[(mousepos[1]+vector[0])*cols+mousepos[0]+vector[1]].highlight(False) 



			if not lost and not won:
				if not started:
					start = datetime.datetime.now()
				else:
					elapsed_time=datetime.datetime.now()-start
			window.fill((0, 0, 0))
			bar.update(bombs_counter, elapsed_time)
			bar.draw(window)
			field_list.draw(window)
			if lost or won:
				end.draw(window,elapsed_time)
			pygame.display.flip()

if __name__ == "__main__":
	main()
