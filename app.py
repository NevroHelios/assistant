import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pygame

import os
os.environ['PYGAME_DETECT_AVX2'] = '1'

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dark-Themed Application")
        self.geometry("800x600")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.speak_tab = ctk.CTkFrame(self.notebook)
        self.generate_tab = ctk.CTkFrame(self.notebook)
        self.audio_tab = ctk.CTkFrame(self.notebook)

        self.notebook.add(self.speak_tab, text="Speak")
        self.notebook.add(self.generate_tab, text="Generate Text")
        self.notebook.add(self.audio_tab, text="Generate Audio")

        # Speak Tab
        self.create_speak_tab()

        # Generate Text Tab
        self.create_generate_tab()

        # Generate Audio Tab
        self.create_audio_tab()

        # Configure row and column weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_speak_tab(self):
        self.speak_tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.speak_tab.grid_rowconfigure((1, 2), weight=1)

        # Buttons
        self.speak_button = ctk.CTkButton(self.speak_tab, text="Speak", command=self.speak_function)
        self.speak_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.pause_button = ctk.CTkButton(self.speak_tab, text="Pause", command=self.pause_function)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.finish_button = ctk.CTkButton(self.speak_tab, text="Finish", command=self.finish_function)
        self.finish_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Text fields
        self.output1 = ctk.CTkTextbox(self.speak_tab, wrap="word")
        self.output1.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.output2 = ctk.CTkTextbox(self.speak_tab, wrap="word")
        self.output2.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Audio player (placeholder)
        self.audio_player = ctk.CTkFrame(self.speak_tab)
        self.audio_player.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.audio_player, text="Audio Player Placeholder").pack()

    def create_generate_tab(self):
        self.generate_tab.grid_columnconfigure(0, weight=1)
        self.generate_tab.grid_rowconfigure((0, 1), weight=1)

        self.input_text = ctk.CTkTextbox(self.generate_tab, wrap="word")
        self.input_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.generate_button = ctk.CTkButton(self.generate_tab, text="Generate Text", command=self.generate_text)
        self.generate_button.grid(row=1, column=0, padx=5, pady=5)

        self.output_text = ctk.CTkTextbox(self.generate_tab, wrap="word")
        self.output_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

    def create_audio_tab(self):
        self.audio_tab.grid_columnconfigure(0, weight=1)
        self.audio_tab.grid_rowconfigure((0, 1, 2), weight=1)

        self.audio_input = ctk.CTkTextbox(self.audio_tab, wrap="word")
        self.audio_input.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.generate_audio_button = ctk.CTkButton(self.audio_tab, text="Generate Audio", command=self.generate_audio)
        self.generate_audio_button.grid(row=1, column=0, padx=5, pady=5)

        self.audio_player_frame = ctk.CTkFrame(self.audio_tab)
        self.audio_player_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(self.audio_player_frame, text="Audio Player Placeholder").pack()

    def speak_function(self):
        # Placeholder function
        self.output1.delete("1.0", tk.END)
        self.output2.delete("1.0", tk.END)
        self.output1.insert(tk.END, "This is the first output string from the speak function.")
        self.output2.insert(tk.END, "This is the second output string from the speak function.")

    def pause_function(self):
        print("Pause function called")

    def finish_function(self):
        print("Finish function called")

    def generate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        # Placeholder function
        generated_text = f"Generated text based on input: {input_text}"
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, generated_text)

    def generate_audio(self):
        input_text = self.audio_input.get("1.0", tk.END).strip()
        # Placeholder function
        print(f"Generating audio for: {input_text}")
        # Here you would typically generate an audio file
        # For now, we'll just update the placeholder text
        for widget in self.audio_player_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.audio_player_frame, text="Audio generated and ready to play").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()