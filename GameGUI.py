import sys
import os
import random
from tkinter import Tk, Label, Button, Frame, Entry, ttk, BooleanVar, Checkbutton, Canvas
from PIL import Image, ImageTk
import pygame

module_path = r"D:\Course-Work\build\Debug"
if module_path not in sys.path:
    sys.path.append(module_path)
    
from game_module import Game
from visualization import plot_scores
# Ініціалізувати випадковий генератор
random.seed()
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Who is Smaller? Game")

        # Встановлюємо сталі розміри вікна
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.mode = None
        self.game = None
        self.player1_name = None
        self.player2_name = None

        # Контейнер для таблиці історії
        self.history_frame = Frame(self.root,bg="#E0F7FA")
        self.history_frame.pack(side="bottom", fill="x", pady=10)
        self.tree = None

        # Ініціалізація звуку
        self.sound_enabled = BooleanVar(value=True)
        self.init_music()

        # Головне меню
        self.main_menu()

    def init_music(self):
        pygame.mixer.init()
        music_path = "D:/Course-Work/music/waiting-time-175800.mp3"
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        else:
            print("Музичний файл не знайдено:", music_path)

    def main_menu(self):
        # Видалення таблиці історії, якщо вона є
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        # Очистка вікна
        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()
        # Додавання фону
        self.root.configure(bg="#E0F7FA") 
        Label(self.root, text="Гра. Хто менше?", font=("Helvetica", 16), bg="#E0F7FA").pack(pady=20)
        button_frame = Frame(self.root, bg="#E0F7FA")
        button_frame.pack(pady=50)

        Button(
            button_frame,
            text="1 Гравець",
            font=("Helvetica", 15),
            command=lambda: self.set_mode("single"),
            bg="#00ffff"
        ).pack(side="left", padx=100)

        Button(
            button_frame,
            text="2 Гравці",
            font=("Helvetica", 15),
            command=lambda: self.set_mode("two"),
            bg="#00ffff"
        ).pack(side="left", padx=100)

        settings_exit_frame = Frame(self.root, bg="#E0F7FA")
        settings_exit_frame.pack(pady=20)

        Button(
            settings_exit_frame,
            text="Налаштування",
            font=("Helvetica", 15),
            command=self.settings_menu,
            bg="#00ffff"
        ).pack(pady=10, fill="x", padx=50)
        
        Button(
            settings_exit_frame,
            text="Правила",
            font=("Helvetica", 15),
            command=self.rules_menu,
            bg="#00ffff"
        ).pack(pady=10, fill="x", padx=50)

        Button(
            settings_exit_frame,
            text="Вихід",
            font=("Helvetica", 15),
            command=self.root.quit,
            bg="#00ffff"
        ).pack(pady=10, fill="x", padx=50)

    def rules_menu(self):
        # Очистка вікна
        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()

        self.root.configure(bg="#E0F7FA")

        Label(self.root, text="Правила", font=("Helvetica", 18), bg="#E0F7FA").pack(pady=20)
        
        rules_text = (
            "Хто менше?\n\n"
            "Гравці загадавши по одному числу від 1 до 5, порівнюють їх.\n"
            "Якщо числа співпадають або різняться більше, ніж на одиницю, кожен гравець "
            "отримує кількість очок, рівну його загаданому числу.\n"
            "Якщо ж числа різняться на одиницю, то гравець, який обрав менше число, "
            "отримує очки, рівні сумі загаданих чисел.\n"
            "Гра триває десять турів, і після кожного з них очки сумуються.\n"
            "Перемагає гравець, який набрав більше очок."
        )

        Label(self.root, text=rules_text, font=("Helvetica", 13), justify="center", wraplength=600, bg="#E0F7FA").pack(pady=10)

        Button(
            self.root,
            text="Повернутися до головного меню",
            font=("Helvetica", 12),
            command=self.main_menu,
            bg="#00ffff"
        ).pack(pady=10)

    def settings_menu(self):
        # Очистка вікна
        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()

        self.root.configure(bg="#E0F7FA")
        Label(self.root, text="Налаштування", font=("Helvetica", 16), bg="#E0F7FA").pack(pady=20)

        Checkbutton(
            self.root,
            text="Увімкнути звук",
            font=("Helvetica", 16),
            variable=self.sound_enabled,
            command=lambda: pygame.mixer.music.unpause() if self.sound_enabled.get() else pygame.mixer.music.pause(),
            bg="#E0F7FA",
        ).pack(pady=10)

        Button(
            self.root,
            text="Повернутися до головного меню",
            font=("Helvetica", 12),
            command=self.main_menu,
            bg="#00ffff"
        ).pack(pady=10)


    def set_mode(self, mode):
        self.mode = mode
        self.ask_names(single_player=(mode == "single"))

    def ask_names(self, single_player):
        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()

        Label(self.root, text="Введіть імена гравців", font=("Helvetica", 14),bg="#E0F7FA").pack(pady=10)

        name_frame = Frame(self.root, bg="#E0F7FA")
        name_frame.pack(pady=20)

        Label(name_frame, text="Гравець 1:", font=("Helvetica", 12),bg="#E0F7FA").grid(row=0, column=0, padx=5, pady=5)
        self.player1_name_entry = Entry(name_frame, font=("Helvetica", 12))
        self.player1_name_entry.grid(row=0, column=1, padx=5, pady=5)

        if single_player:
            self.player2_name = "Бот"
        else:
            Label(name_frame, text="Гравець 2:", font=("Helvetica", 12),bg="#E0F7FA").grid(row=1, column=0, padx=5, pady=5)
            self.player2_name_entry = Entry(name_frame, font=("Helvetica", 12))
            self.player2_name_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(
            self.root,
            text="Почати гру",
            font=("Helvetica", 12),
            command=self.save_names_and_start_game,
            bg="#00ffff"
        ).pack(pady=10)

    def save_names_and_start_game(self):
        self.player1_name = self.player1_name_entry.get() or "Гравець 1"
        if self.mode == "two":
            self.player2_name = self.player2_name_entry.get() or "Гравець 2"
        self.start_game()

    def start_game(self):
        self.game = Game(player1_name=self.player1_name, player2_name=self.player2_name)
        self.current_round = 1
        self.rounds = list(range(1, 11))
        self.player1_scores = []
        self.player2_scores = []
        self.history = []

        # Ініціалізувати таблицю історії
        self.initialize_round_history()
        self.play_round()

    def initialize_round_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        columns = ("Раунд", self.player1_name, self.player2_name)
        self.tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", height=5)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")

        self.tree.pack(fill="x", padx=0, pady=0)

    def update_round_history(self):
        self.tree.delete(*self.tree.get_children())  # Очистити таблицю

        for i, (p1, p2) in enumerate(self.history, start=1):
            self.tree.insert("", "end", values=(i, p1, p2))

    def play_round(self):
        if self.current_round > 10:
            self.show_final_results()
            return

        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()

        Label(self.root, text=f"Раунд {self.current_round}", font=("Helvetica", 14),bg="#E0F7FA").pack(pady=10)

        Label(
            self.root,
            text=f"{self.player1_name}, оберіть карту:",
            font=("Helvetica", 12),
            bg="#E0F7FA"
        ).pack(pady=5)

        self.create_button_row(self.process_player1_turn)

    def create_button_row(self, command):
        button_frame = Frame(self.root, bg="#E0F7FA")
        button_frame.pack(pady=10)

        self.button_images = []  

        for i in range(1, 6):
            image_path = f"D:/Course-Work/images/card.png" 
            image = Image.open(image_path)
            image = image.resize((90, 120), Image.Resampling.LANCZOS)  
            photo = ImageTk.PhotoImage(image)

            self.button_images.append(photo) 

            button = Button(
                button_frame,
                text=str(i),
                image=photo,
                compound="center",
                font=("Helvetica", 28, "bold"),
                bg="#00ffff",
                fg="black",
                width=90,
                height=120,
                relief="solid",
                bd=2,
                command=lambda choice=i: command(choice),
            )
            button.pack(side="left", padx=10, pady=40)

    def process_player1_turn(self, choice):
        self.player1_choice = choice

        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()

        Label(self.root, text=f"Раунд {self.current_round}", font=("Helvetica", 14),bg="#E0F7FA").pack(pady=10)

        if self.mode == "two":
            Label(
                self.root,
                text=f"{self.player2_name}, оберіть карту:",
                font=("Helvetica", 12),
                bg="#E0F7FA"
            ).pack(pady=5)

            self.create_button_row(self.process_player2_turn)
        else:
            # повідомлення "Бот обирає..."
            bot_label = Label(
                self.root,
                text=f"{self.player2_name} обирає карту...",
                font=("Helvetica", 12),
                bg="#E0F7FA"
            )
            bot_label.pack(pady=10)

            # затримка перед вибором бота
            self.root.after(900, lambda: self.bot_choose_card(bot_label))

    def bot_choose_card(self, bot_label):
        bot_choice = random.randint(1, 5)
        bot_label.config(text=f"{self.player2_name} обрав карту: {bot_choice}")

        self.root.after(500, lambda: self.process_player2_turn(bot_choice))  


    def process_player2_turn(self, choice):
        player2_choice = choice
        self.add_to_history(self.player1_choice, player2_choice)
        self.current_round += 1
        self.play_round()


    def add_to_history(self, player1_choice, player2_choice):
        self.history.append((player1_choice, player2_choice))
        self.game.playRound(player1_choice, player2_choice)
        scores = self.game.getScores()
        self.player1_scores.append(scores[0])
        self.player2_scores.append(scores[1])

        # Оновити таблицю
        self.update_round_history()
        
    def saveToFile(self):
        filename_frame = Frame(self.root, bg="#E0F7FA")
        filename_frame.pack(pady=20)

        Label(filename_frame, text="Назва файлу:", font=("Helvetica", 12),bg="#E0F7FA").grid(row=0, column=0, padx=5, pady=5)
        filename_entry = Entry(filename_frame, font=("Helvetica", 12))
        filename_entry.grid(row=0, column=1, padx=5, pady=5)

        def onSave():
            filename = filename_entry.get().strip()
            if filename:
                try:
                    self.game.saveGameToFile(filename)
                    print(f"Гру збережено у файл '{filename}'")
                except Exception as e:
                    print(f"Помилка збереження файлу: {e}")
            else:
                print("Назва файлу не може бути порожньою.")

        save_button = Button(filename_frame, text="Зберегти", font=("Helvetica", 12),bg="#00ffff", command=onSave)
        save_button.grid(row=0, column=2, padx=5, pady=5)
    
    def show_final_results(self):
        for widget in self.root.winfo_children():
            if widget != self.history_frame:
                widget.destroy()
        scores = self.game.getScores()
        result_text = f"Фінальні рахунки:\n{self.player1_name}: {scores[0]}\n{self.player2_name}: {scores[1]}"
        if scores[0] > scores[1]:
            result_text += f"\nПереміг {self.player1_name}!"
        elif scores[1] > scores[0]:
            result_text += f"\nПереміг {self.player2_name}!"
        else:
            result_text += "\nНічия!"
        Label(self.root, text=result_text, font=("Helvetica", 14),bg="#E0F7FA").pack(pady=20)
        button_frame = Frame(self.root, bg="#E0F7FA")
        button_frame.pack(pady=20)
        Button(
            button_frame,
            text="Показати графік",
            font=("Helvetica", 15),
            command=self.show_plot,
            bg="#00ffff"
        ).pack(side="left", padx=20)
        Button(
            button_frame,
            text="Повернутися до головного меню",
            font=("Helvetica", 15),
            command=self.main_menu,
            bg="#00ffff"
        ).pack(side="right", padx=20)
        Button(
            button_frame,
            text="Зберегти історію гри",
            font=("Helvetica", 15),
            command=self.saveToFile,
            bg="#00ffff"
        ).pack(side="right", padx=20)


    def show_plot(self):
        plot_scores(self.rounds, self.player1_scores, self.player2_scores, self.player1_name, self.player2_name)