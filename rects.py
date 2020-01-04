import pygame
import random
import copy


class Board:
	# создание поля
	def __init__(self, width):
		self.width = width
		self.board = [[[0, 1] for __ in range(width)] for _ in range(width)]
		# значения по умолчанию
		self.border = 20
		self.extra_top_border = 40
		self.font_size = 30
		self.cell_size = 50
		self.score = 0
		self.running = True
		self.create_screen()
		self.next_move()
		self.colors = {2: (100, 100, 100), 4: (200, 200, 0), 8: (255, 105, 0), 16: (255, 43, 0),
		               32: (21, 171, 0), 64: (178, 102, 255), 128: (255, 8, 127), 256: (46, 139, 90),
		               512: (130, 120, 255), 1024: (0, 0, 255), 2048: (100, 100, 55)
		               }

	def create_screen(self):
		global screen
		width = self.width * self.cell_size + self.border * 2
		height = width + self.extra_top_border
		screen = pygame.display.set_mode((width, height))

	# настройка внешнего вида
	def set_view(self, left, cell_size, font_size):
		self.border = left
		self.cell_size = cell_size
		self.font_size = font_size
		self.create_screen()

	def fill_text_into_cell(self, text, x, y):
		text = str(text)
		fz = self.font_size - len(text)
		font = pygame.font.Font(None, fz)
		text = font.render(text, 1, pygame.Color('white'))
		text_w, text_h = text.get_width(), text.get_height()
		text_x = x * self.cell_size + self.border + (self.cell_size - text_w) // 2
		text_y = y * self.cell_size + self.border + (self.cell_size - text_h) // 2 + self.extra_top_border
		screen.blit(text, (text_x, text_y))

	def display_score(self):
		pygame.draw.rect(screen, pygame.Color('white'), (self.border, 0, self.width * self.cell_size, self.extra_top_border))
		fz = self.font_size + 5 - len(str(self.score))
		font = pygame.font.Font(None, fz)
		text = font.render(str(self.score), 1, pygame.Color('black'))
		text_w, text_h = text.get_width(), text.get_height()
		text_x = self.border + (self.width * self.cell_size - text_w) // 2
		text_y = (self.extra_top_border - text_h) // 2
		screen.blit(text, (text_x, text_y))

	def render(self):
		if not self.running:
			return
		screen.fill((0, 0, 0))
		self.display_score()
		for i in range(self.width):
			for j in range(self.width):
				# координаты клетки
				x = j * self.cell_size + self.border
				y = i * self.cell_size + self.border + self.extra_top_border
				item = self.board[j][i][0]
				if item in self.colors:
					pygame.draw.ellipse(screen, self.colors[item], (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
				if item:
					self.fill_text_into_cell(item, j, i)
		pygame.display.flip()

	def next_move(self):
		empty = self.get_empty(self.board)
		if empty:
			x, y = random.choice(empty)
			self.board[y][x] = [random.choice([2, 4]), 1]
			if not self.check_if_lose():
				return
		self.render()
		self.lose()

	def get_empty(self, board):
		empty = []
		for i in range(len(board)):
			for j in range(len(board)):
				if not board[i][j][0]:
					empty.append((j, i))
		return empty

	def check_if_lose(self):
		# если пустых клеток нет
		if not self.get_empty(self.board):
			for vector in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
				if self.get_empty(self.fake_board(vector)):
					# если хотя бы при одном варианте хода появятся пустые клетки
					return False
			# если не появятся
			return True
		# если есть пустые клетки
		return False

	def check_if_win(self):
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j][0] >= 2048:
					return True
		return False

	def fake_board(self, vector):
		board = copy.deepcopy(self.board)
		board = list(list([j[0], 1] for j in i) for i in board)
		self.merge(vector, board)
		return board

	def lose(self):
		text = 'Вы проиграли'
		self.alert(text)
		self.running = False

	def win(self):
		text = 'Вы выиграли'
		self.alert(text)
		self.running = False

	def alert(self, text):
		fz = self.width * 7
		font = pygame.font.Font(None, fz)
		text = font.render(text, 1, pygame.Color('white'))
		text_w, text_h = text.get_width(), text.get_height()
		text_x = (self.cell_size * self.width + self.border - text_w) // 2
		text_y = (self.cell_size * self.width + self.border - text_h) // 2
		pygame.draw.rect(screen, (200, 0, 0), (text_x - 5, text_y - 5, text_w + 10, text_h + 10))
		pygame.draw.rect(screen, (0, 200, 0), (text_x - 5, text_y - 5, text_w + 10, text_h + 10), 4)
		screen.blit(text, (text_x, text_y))
		pygame.display.flip()

	def merge(self, vector, board, auto_render=0):
		x, y = vector
		before = copy.deepcopy(board)
		# board = list(list([j, 1] for j in i) for i in board)
		x_range = range(len(board))
		y_range = range(len(board))
		if not x:
			if y == 1:
				y_range = range(len(board) - 2, -1, -1)
			elif y == -1:
				y_range = range(1, len(board))
		elif not y:
			if x == 1:
				x_range = range(len(board) - 2, -1, -1)
			elif x == -1:
				x_range = range(1, len(board))
		for i in y_range:
			for j in x_range:
				item, item_is_allowed_to_merge = board[i][j]
				new, new_is_allowed_to_merge = board[i + y][j + x]
				if not item:
					continue
				elif not new:
					board[i][j] = [0, 1]
					board[i + y][j + x] = [item, item_is_allowed_to_merge]
				elif new == item and item_is_allowed_to_merge and new_is_allowed_to_merge:
					board[i][j] = [0, 1]
					board[i + y][j + x] = [item * 2, 0]
					if auto_render:
						self.score += item * 2
		if auto_render:
			self.render()
		if before != board:
			self.merge(vector, board, auto_render)

	def move(self, key):
		if key == 273:
			vector = (-1, 0)
		elif key == 274:
			vector = (1, 0)
		elif key == 275:
			vector = (0, 1)
		elif key == 276:
			vector = (0, -1)
		else:
			vector = 0
		if key in range(273, 277):
			self.board = list(list([j[0], 1] for j in i) for i in self.board)
			self.merge(vector, self.board, 1)
			self.next_move()


pygame.init()
screen = 0
board = Board(4)
# board.set_view(10, 50, 25)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYUP:
			board.move(event.key)
	board.render()
pygame.quit()
