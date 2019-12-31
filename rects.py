import pygame
import random
import copy
import itertools


class Board:
	# создание поля
	def __init__(self, width):
		self.width = width
		# self.board = [[random.choice([2 ** random.randint(1, 10), 0]) for _ in range(width)] for _ in range(width)]
		self.board = [[0] * width for _ in range(width)]
		# значения по умолчанию
		self.border = 10
		self.font_size = 30
		self.cell_size = 50
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
		screen = pygame.display.set_mode((width, width))

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
		text_y = y * self.cell_size + self.border + (self.cell_size - text_h) // 2
		screen.blit(text, (text_x, text_y))

	def next_move(self):
		empty = self.get_empty(self.board)
		if empty:
			x, y = random.choice(empty)
			variants = set(itertools.chain(*self.board))
			variants.add(2)
			variants.discard(0)
			self.board[y][x] = random.choice(list(variants))
			if not self.check_if_lose():
				return
		self.lose()

	def get_empty(self, board):
		empty = []
		for i in range(self.width):
			for j in range(self.width):
				if not board[i][j]:
					empty.append((j, i))
		return empty

	def check_if_lose(self):
		# если пустых клеток нет
		if not self.get_empty(self.board):
			for vector in itertools.product(range(2), range(2)):
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
				if self.board[i][j] >= 2048:
					return True
		return False

	def fake_board(self, vector):
		board = copy.deepcopy(self.board)
		self.shift(vector, board)
		return board

	def render(self):
		if not self.running:
			return
		screen.fill((0, 0, 0))
		for i in range(self.width):
			for j in range(self.width):
				# координаты клетки
				x = j * self.cell_size + self.border
				y = i * self.cell_size + self.border
				item = self.board[j][i]
				if item:
					pygame.draw.ellipse(screen, self.colors[item], (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
				if item:
					self.fill_text_into_cell(item, j, i)
		pygame.display.flip()

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

	def shift_one(self, vector, x, y, board):
		x_possible, y_possible = x + vector[0], y + vector[1]
		try:
			possible = board[y_possible][x_possible]
			item = board[y][x]
		except IndexError:
			return
		if possible == 0:
			new = item
			old = 0
		elif possible == item:
			new = item * 2
			old = 0
		else:
			new = possible
			old = item
		board[y][x] = old
		board[y_possible][x_possible] = new
		if not possible:
			self.shift_one(vector, x_possible, y_possible, board)

	def shift_col(self, y, i, board):
		for j in range(self.width):
			self.shift_one((0, y), j, i, board)

	def shift_row(self, x, j, board):
		for i in range(self.width):
			self.shift_one((x, 0), j, i, board)

	def shift(self, vector, board):
		for i in range(1, self.width):
			if vector == (1, 0):
				self.shift_col(1, self.width - i - 1, board)
			elif vector == (-1, 0):
				self.shift_col(-1, i, board)
			elif vector == (0, 1):
				self.shift_row(1, self.width - i - 1, board)
			elif vector == (0, -1):
				self.shift_row(-1, i, board)

	def move(self, key):
		if key == 273:
			vector = (0, -1)
		elif key == 274:
			vector = (0, 1)
		elif key == 275:
			vector = (1, 0)
		elif key == 276:
			vector = (-1, 0)
		else:
			vector = (0, 0)
		self.shift(vector, self.board)
		self.next_move()

	def get_cell(self, mouse_pos):
		x, y = mouse_pos
		# - border
		x -= self.border
		y -= self.border
		# если клик не по полю
		if not 0 <= x <= self.width * self.cell_size or not 0 <= y <= self.width * self.cell_size:
			return None
		# indexes
		i = y // self.cell_size
		j = x // self.cell_size
		return j, i

	def on_click(self, cell_coords):
		if cell_coords is None:
			return
		x, y = cell_coords
		# 1 на 0, 0 на 1
		for i in range(self.width):
			self.board[i][x] = 1 - self.board[i][x]
		for j in range(self.width):
			self.board[y][j] = 1 - self.board[y][j]
		self.board[y][x] = 1 - self.board[y][x]

	def get_click(self, mouse_pos):
		# координаты клетки
		cell = self.get_cell(mouse_pos)
	# обработка
	# self.on_click(cell)


pygame.init()
screen = 0
board = Board(4)
# board.set_view(10, 50, 25)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# обработка кликов
			board.get_click(event.pos)
		if event.type == pygame.KEYUP:
			board.move(event.key)
	board.render()
pygame.quit()
