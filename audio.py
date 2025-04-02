import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import pyttsx3
import re
import os

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Function to extract text from PDF
def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        chapters = re.split(r"\bCHAPTER\s+\d+\b", full_text, flags=re.IGNORECASE)
        return [ch.strip() for ch in chapters if ch.strip()]

# Function to save audiobook
def save_as_audio(text, filename, voice_id):
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 170)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    os.system(f"start {filename}")

# File picker
def pick_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_label.config(text=file_path)
        app.selected_file = file_path

# Main action
def generate_audiobook():
    if not hasattr(app, 'selected_file'):
        messagebox.showerror("Oops!", "Please select a PDF file first.")
        return

    voice_index = voice_var.get()
    if voice_index == "":
        messagebox.showerror("Oops!", "Please select a voice.")
        return

    chapters = read_pdf(app.selected_file)
    for i, chapter_text in enumerate(chapters, start=1):
        filename = f"chapter_{i}.mp3"
        save_as_audio(chapter_text, filename, voices[int(voice_index)].id)
        messagebox.showinfo("Yay!", f"Saved {filename} 💕")

# GUI Setup
app = tk.Tk()
app.title("Skye's Kawaii Audiobook Maker 🎀")
app.geometry("500x500")
app.configure(bg="#fae8e0")

title = tk.Label(app, text="📚 Make Your Own Audiobook!", font=("Helvetica", 18, "bold"), bg="#fae8e0", fg="#ef7c8e")
title.pack(pady=20)

file_btn = tk.Button(app, text="Choose PDF", command=pick_file, bg="#ef7c8e", fg="white", font=("Helvetica", 12, "bold"))
file_btn.pack(pady=10)

file_label = tk.Label(app, text="No file selected", bg="#fae8e0", fg="#666", wraplength=400)
file_label.pack(pady=5)

# Voice Dropdown
tk.Label(app, text="Choose a voice:", bg="#fae8e0", fg="#ef7c8e", font=("Helvetica", 12, "bold")).pack(pady=10)

voice_var = tk.StringVar()
voice_menu = tk.OptionMenu(app, voice_var, *[f"{i} - {v.name}" for i, v in enumerate(voices)])
voice_menu.config(bg="#f8c8dc", fg="black", font=("Helvetica", 10))
voice_menu.pack(pady=5)

# Convert Button
convert_btn = tk.Button(app, text="✨ Convert to Audiobook ✨", command=generate_audiobook,
                        bg="#ef7c8e", fg="white", font=("Helvetica", 14, "bold"), padx=10, pady=5)
convert_btn.pack(pady=30)

app.mainloop()




    