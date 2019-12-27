import pygame
import random


class Board:
	# создание поля
	def __init__(self, width):
		self.width = width
		self.board = [[random.choice([2 ** random.randint(1, 10), 0]) for _ in range(width)] for _ in range(width)]
		# self.board = [[0] * width for _ in range(width)]
		self.board[5][5] = 4
		# значения по умолчанию
		self.border = 10
		self.font_size = 30
		self.cell_size = 50
		self.create_screen()

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

	def fill_text(self, text, x, y):
		text = str(text)
		fz = self.font_size - len(text)
		font = pygame.font.Font(None, fz)
		text = font.render(text, 1, pygame.Color('white'))
		text_w, text_h = text.get_width(), text.get_height()
		text_x = x * self.cell_size + self.border + (self.cell_size - text_w) // 2
		text_y = y * self.cell_size + self.border + (self.cell_size - text_h) // 2
		screen.blit(text, (text_x, text_y))

	def render(self):
		for i in range(self.width):
			for j in range(self.width):
				# координаты клетки
				x = j * self.cell_size + self.border
				y = i * self.cell_size + self.border
				item = self.board[j][i]
				# pygame.draw.ellipse(screen, (item * 255 / 2048, 255, 255), (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
				pygame.draw.ellipse(screen, (230, 230, 230), (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2), 2)
				if item:
					self.fill_text(item, j, i)
				# self.fill_text(2 ** random.randint(1, 10), j, i)
		pygame.display.flip()

	def shift_one(self, vector, x, y):
		x_possible, y_possible = x + vector[0], y + vector[1]
		try:
			possible = self.board[y_possible][x_possible]
			item = self.board[y][x]
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
		self.board[y][x] = old
		self.board[y_possible][x_possible] = new
		if not possible:
			self.shift_one(vector, x_possible, y_possible)

	def shift_col(self, y, i):
		for j in range(self.width):
			self.shift_one((0, y), j, i)

	def shift_row(self, x, j):
		for i in range(self.width):
			self.shift_one((x, 0), j, i)

	def shift(self, vector):
		for i in range(1, self.width):
			if vector == (1, 0):
				self.shift_col(1, self.width - i - 1)
			elif vector == (-1, 0):
				self.shift_col(-1, i)
			elif vector == (0, 1):
				self.shift_row(1, self.width - i - 1)
			elif vector == (0, -1):
				self.shift_row(-1, i)

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
		# print(vector)
		self.shift(vector)

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
board = Board(10)
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
	screen.fill((0, 0, 0))
	board.render()
	pygame.display.flip()

pygame.quit()
