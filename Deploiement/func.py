from PIL import Image
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import fleep
from mutagen import File
import subprocess


def is_valid_media(filepath):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except:
        return False

def is_audio_file(filepath):
    with open(filepath, "rb") as file:
        info = fleep.get(file.read(128))
        # print(f"File: {filepath}, Type: {info.type}")
    return "audio" in info.type or "video" in info.type  # Some audio files may be classified as video

# def open_file(label):
#     try:
#         file_paths = filedialog.askopenfilenames(
#             title="Select audio files",
#             filetypes=[("All files", "*.*")]
#         )
#         valid_files = {}
#         for path in file_paths:
#             if is_audio_file(path) and is_valid_media(path):
#                 valid_files[path] = False # False indicates not liked yet
#         # print("Valid audio files:", valid_files)
#         label.configure(text=f"{len(valid_files)} fichiers choisis",fg_color=("gray20", "gray80"))
#         return valid_files
#     except Exception as e:
#         # print("Error:", e)
#         # label.configure(text="Error opening files")
#         show_toast(label.master, "Erreur lors de l'ouverture des fichiers")
#         return {}

def open_file(root, valid_files=None):
    if valid_files is None:
        valid_files = {}
    
    try:
        file_paths = filedialog.askopenfilenames(
            title="Select audio files",
            filetypes=[("All files", "*.*")]
        )
        
        invalid_count = 0

        for path in file_paths:
            if path in valid_files:
                continue  # éviter doublons

            if is_audio_file(path) and is_valid_media(path):
                valid_files[path] = False
            else:
                invalid_count += 1
        
        # if len(valid_files) > 0:
        #     label.configure(text=f"{len(valid_files)} fichiers importé(s)")

        if invalid_count > 0:
            show_toast(root, f"{invalid_count} fichiers ignorés")
        elif len(valid_files) == 0:
            show_toast(root, "Aucun fichier audio valide sélectionné")
        
        return valid_files

    except Exception:
        show_toast(root, "Erreur lors de l'ouverture des fichiers")
        return {}

# def fade_color(widget, start_color, end_color, steps=20, delay=20):
#     import time

#     def hex_to_rgb(hex_color):
#         hex_color = hex_color.lstrip("#")
#         return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

#     def rgb_to_hex(rgb):
#         return "#%02x%02x%02x" % rgb

#     start = hex_to_rgb(start_color)
#     end = hex_to_rgb(end_color)

#     # Chaque appel génère un token unique
#     token = object()
#     widget._fade_token = token

#     def step(i):
#         # Si un nouvel appel a démarré, on abandonne cette animation
#         if getattr(widget, "_fade_token", None) is not token:
#             return
#         if i > steps:
#             return

#         ratio = i / steps
#         new_color = tuple(
#             int(start[j] + (end[j] - start[j]) * ratio) for j in range(3)
#         )
#         widget.configure(fg_color=rgb_to_hex(new_color))
#         widget.after(delay, lambda: step(i + 1))

#     step(0)

def show_toast(root, message, duration=3000):

    error_icon = ctk.CTkImage(Image.open("assets/error.png"), size=(20, 20))

    toast = ctk.CTkToplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)

    frame = ctk.CTkFrame(toast, corner_radius=10,border_width=2, border_color="#F36C19")
    frame.pack(padx=0, pady=0, fill="both", expand=True)
    bg = root.cget("fg_color")

    if isinstance(bg, tuple):
        bg = bg[0]  # mode light/dark safe

    toast.configure(fg_color=bg)
    frame.configure(fg_color=bg)

    label = ctk.CTkLabel(
        frame,
        text=message,
        text_color="#F36C19",
        image=error_icon,
        compound="left",
        font=("Arial", 12)
    )
    label.pack(padx=15, pady=10)

    root.update()  
    toast.update_idletasks()

    x = root.winfo_rootx() + root.winfo_width() - toast.winfo_width() - 20
    y = root.winfo_rooty() + root.winfo_height() - toast.winfo_height() - 20

    toast.geometry(f"{toast.winfo_width()}x{toast.winfo_height()}+{x}+{y}")

    toast.after(duration, toast.destroy)

