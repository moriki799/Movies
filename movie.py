import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

# Создаем главное окно
root = tk.Tk()
root.title("Movie Library")

# Переменные для ввода данных
title_var = tk.StringVar()
genre_var = tk.StringVar()
year_var = tk.StringVar()
rating_var = tk.StringVar()

# Ввод данных о фильме
tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=title_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=genre_var).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=year_var).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Рейтинг").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=rating_var).grid(row=3, column=1, padx=5, pady=5)

# Таблица для отображения фильмов
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Поля для фильтрации
tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5)
filter_genre_var = tk.StringVar()
tk.Entry(root, textvariable=filter_genre_var).grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по году").grid(row=7, column=0, padx=5, pady=5)
filter_year_var = tk.StringVar()
tk.Entry(root, textvariable=filter_year_var).grid(row=7, column=1, padx=5, pady=5)

# Список для хранения фильмов
movies = []

# Загружаем данные из файла при запуске
def load_from_json():
    global movies
    try:
        with open("movies.json", "r", encoding='utf-8') as f:
            movies = json.load(f)
        # Очищаем таблицу
        for item in tree.get_children():
            tree.delete(item)
        # Добавляем из файла
        for m in movies:
            tree.insert('', 'end', values=(m['Название'], m['Жанр'], m['Год'], m['Рейтинг']))
    except FileNotFoundError:
        movies.clear()

# Сохраняем данные в файл
def save_to_json():
    with open("movies.json", "w", encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# Добавление фильма
def add_movie():
    title = title_var.get()
    genre = genre_var.get()
    year = year_var.get()
    rating = rating_var.get()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    # Проверка
    try:
        year_int = int(year)
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом")
        return

    try:
        rating_float = float(rating)
        if not (0 <= rating_float <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
        return

    # Добавляем в список
    movie = {
        'Название': title,
        'Жанр': genre,
        'Год': year_int,
        'Рейтинг': rating_float
    }
    movies.append(movie)
    # Обновляем таблицу
    tree.insert('', 'end', values=(title, genre, year_int, rating_float))
    # Очистка полей
    title_var.set('')
    genre_var.set('')
    year_var.set('')
    rating_var.set('')
    # Сохраняем
    save_to_json()

# Фильтр
def apply_filter():
    genre_filter = filter_genre_var.get().lower()
    year_filter = filter_year_var.get()

    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)

    for m in movies:
        match_genre = True
        match_year = True
        if genre_filter:
            match_genre = genre_filter in m['Жанр'].lower()
        if year_filter:
            match_year = str(m['Год']) == year_filter
        if match_genre and match_year:
            tree.insert('', 'end', values=(m['Название'], m['Жанр'], m['Год'], m['Рейтинг']))

# Загружаем данные сразу при запуске
load_from_json()
apply_filter()

# Размещение кнопок
tk.Button(root, text="Добавить фильм", command=add_movie).grid(row=4, column=0, padx=5, pady=10)
tk.Button(root, text="Применить фильтр", command=apply_filter).grid(row=8, column=0, padx=5, pady=10)
tk.Button(root, text="Сохранить", command=save_to_json).grid(row=9, column=0, padx=5, pady=10)

# Запуск интерфейса
root.mainloop()
def load_from_json():
    global movies
    if os.path.exists("movies.json"):
        # Проверяем, что файл не пустой
        if os.path.getsize("movies.json") > 0:
            try:
                with open("movies.json", "r", encoding='utf-8') as f:
                    movies = json.load(f)
            except json.JSONDecodeError:
                # Если файл содержит некорректный JSON, очищаем список
                movies = []
        else:
            # Файл пустой
            movies = []
    else:
        # Файл не существует
        movies = []

    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)
        
    # Вставляем данные
    for m in movies:
        tree.insert('', 'end', values=(m['Название'], m['Жанр'], m['Год'], m['Рейтинг']))

