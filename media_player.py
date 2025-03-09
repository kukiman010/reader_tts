import tkinter as tk
from tkinter import messagebox
import pygame
# from book import Book  

# Инициализация pygame для воспроизведения звука
pygame.mixer.init()

class BookReaderApp:
    def __init__(self, root, book):
        self.root = root
        self.book = book
        self.sentences = list(self.book.iter_sentences())
        self.current_idx = 0
        self.paused = False

        self.root.title(f"Book Reader: {book.title}")

        # Виджет Text для отображения текста
        self.text_area = tk.Text(root, wrap='word', height=20, width=80, font=("Arial", 12))
        self.text_area.pack(padx=20, pady=20)

        # Заполняем все предложения в Text виджете
        for i, sentence in enumerate(self.sentences):
            self.text_area.insert(tk.END, sentence.text + "\n")

        self.text_area.config(state=tk.DISABLED)  # Делаем текст неизменяемым

        # Кнопка паузы/возобновления
        self.pause_btn = tk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(pady=10)

        # Запускаем автоматическое воспроизведение
        self.play_audio()

    def play_audio(self):
        """Проигрывает аудио, связанное с текущим предложением."""
        if self.current_idx < len(self.sentences):
            sentence = self.sentences[self.current_idx]

            if sentence.audio_path:
                self.highlight_sentence(sentence.text)

                try:
                    pygame.mixer.music.load(sentence.audio_path)
                    pygame.mixer.music.play()

                    self.check_audio_end()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not play audio: {e}")

    def check_audio_end(self):
        """Проверяет, закончилось ли воспроизведение."""
        if not self.paused and not pygame.mixer.music.get_busy():
            self.current_idx += 1
            self.play_audio()
        else:
            # Проверяем состояние снова после небольшой задержки
            self.root.after(1000, self.check_audio_end)

    def highlight_sentence(self, sentence_text):
        """Выделяет текущее предложение."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.tag_remove("highlight", 1.0, tk.END)  

        start_idx = self.text_area.search(sentence_text, 1.0, tk.END)
        if start_idx:
            end_idx = f"{start_idx}+{len(sentence_text)}c"
            self.text_area.tag_add("highlight", start_idx, end_idx)
            self.text_area.tag_configure("highlight", background="yellow")
            self.text_area.see(start_idx)  

        self.text_area.config(state=tk.DISABLED)

    def toggle_pause(self):
        """Переключает состояние паузы/воспроизведения."""
        if self.paused:
            pygame.mixer.music.unpause()
            self.pause_btn.config(text="Pause")
            self.paused = False
            self.check_audio_end()  
        else:
            pygame.mixer.music.pause()
            self.pause_btn.config(text="Play")
            self.paused = True
