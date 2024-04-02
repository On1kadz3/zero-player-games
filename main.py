import tkinter as tk
import random

# Размеры поля
WIDTH = 700
HEIGHT = 700

# Размеры клетки
CELL_SIZE = 10

# Вычисление количества клеток в ширину и высоту
CELLS_X = WIDTH // CELL_SIZE
CELLS_Y = HEIGHT // CELL_SIZE

# Создание двумерного массива для поля
field = [[0] * CELLS_X for _ in range(CELLS_Y)]

# Флаг паузы
paused = False

# Функция для обновления состояния поля
def update_field():
    new_field = [[0] * CELLS_X for _ in range(CELLS_Y)]
    for y in range(CELLS_Y):
        for x in range(CELLS_X):
            # Подсчет количества соседей
            neighbors = sum([
                field[(y + dy) % CELLS_Y][(x + dx) % CELLS_X]
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0)
            ])
            # Правила игры "Жизнь"
            if field[y][x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_field[y][x] = 0
                else:
                    new_field[y][x] = 1
            else:
                if neighbors == 3:
                    new_field[y][x] = 1
    return new_field


# Функция для обновления состояния поля и отображения его на холсте
def update_canvas():
    global field
    field = update_field()
    canvas.delete("all")
    for y in range(CELLS_Y):
        for x in range(CELLS_X):
            if field[y][x] == 1:
                canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill="black"
                )
    canvas.after(100, update_canvas)

# Заполнение поля случайными клетками
for y in range(CELLS_Y):
    for x in range(CELLS_X):
        if random.random() < 0.5:
            field[y][x] = 1


# Функция для обработки нажатия курсора
def handle_click(event):
    global field
    if paused:
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if field[y][x] == 1:
            field[y][x] = 0
        else:
            field[y][x] = 1


# Функция для обработки нажатия клавиши "P" для паузы
def toggle_pause(event):
    global paused
    paused = not paused


# Создание окна
window = tk.Tk()
window.title("Game of Life")

# Создание холста
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

# Привязка обработчиков событий
canvas.bind("<Button-1>", handle_click)
window.bind("p", toggle_pause)

# Запуск обновления состояния поля и отображения на холсте
update_canvas()

# Запуск главного цикла приложения
window.mainloop()
