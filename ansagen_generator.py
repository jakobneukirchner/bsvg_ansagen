import os
import time
import tkinter as tk
from tkinter import messagebox, ttk
from pygame import mixer

# Lokaler Pfad zu den Audio-Dateien
BASE_PATH = r"C:\Users\jneuk\SysServices\05_BSVG_Ansagen_Service"

# Initialisierung des Audioplayers
mixer.init()

def get_audio_path(category, filename):
    return os.path.join(BASE_PATH, category, filename)

def play_audio_sequence(filepaths):
    for i, filepath in enumerate(filepaths):
        if not os.path.exists(filepath):
            print(f"Fehlt: {filepath}")
            continue
        mixer.music.load(filepath)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
        # Kurze Pause vor Sonderansage (nur wenn nächster Pfad aus "Hinweise" kommt)
        if i + 1 < len(filepaths) and "Hinweise" in filepaths[i + 1]:
            time.sleep(0.5)  # 0.5 Sekunden Pause

def generate_and_play():
    line = combo_line.get().strip()
    destination = combo_destination.get().strip().lower()
    via = combo_via.get().strip().lower()
    is_special = var_special.get()
    selected_special = combo_special.get().strip()

    files = []

    if line:
        line_path = get_audio_path("Nummern/line_number_end", f"{line}.mp3")
        if not os.path.exists(line_path):
            messagebox.showerror("Fehler", f"Linie {line} existiert nicht als Audio-Datei.")
            return
        files.append(get_audio_path("Fragmente", "linie.mp3"))
        files.append(line_path)
    else:
        files.append(get_audio_path("Fragmente", "zug.mp3"))

    if destination:
        dest_path = get_audio_path("Ziele", f"{destination}.mp3")
        if not os.path.exists(dest_path):
            messagebox.showerror("Fehler", f"Zielhaltestelle '{destination}' existiert nicht.")
            return
        files.append(get_audio_path("Fragmente", "nach.mp3"))
        files.append(dest_path)

        if via:
            via_path = get_audio_path("Ziele", f"{via}.mp3")
            if not os.path.exists(via_path):
                messagebox.showerror("Fehler", f"Via-Haltestelle '{via}' existiert nicht.")
                return
            files.append(get_audio_path("Fragmente", "ueber.mp3"))
            files.append(via_path)

    if is_special and selected_special:
        hint_path = get_audio_path("Hinweise", selected_special)
        if not os.path.exists(hint_path):
            messagebox.showerror("Fehler", f"Sonderansage '{selected_special}' nicht gefunden.")
            return
        files.append(hint_path)

    play_audio_sequence(files)

def play_special_only():
    selected_special = combo_special.get().strip()
    if not selected_special:
        messagebox.showerror("Fehler", "Bitte eine Sonderansage auswählen.")
        return
    filepath = get_audio_path("Hinweise", selected_special)
    if not os.path.exists(filepath):
        messagebox.showerror("Fehler", f"Sonderansage '{selected_special}' nicht gefunden.")
        return
    play_audio_sequence([filepath])

# GUI erstellen
root = tk.Tk()
root.title("Ansagen-Generator")
root.geometry("450x500")

# Linienauswahl
label_line = tk.Label(root, text="Liniennummer:")
label_line.pack()
combo_line = ttk.Combobox(root, values=["", "1", "2", "3", "4", "5", "10"])
combo_line.pack()

# Zielhaltestelle
label_destination = tk.Label(root, text="Zielhaltestelle:")
label_destination.pack()
combo_destination = ttk.Combobox(root)
combo_destination.pack()

# Via-Haltestelle
label_via = tk.Label(root, text="Via-Haltestelle (optional):")
label_via.pack()
combo_via = ttk.Combobox(root)
combo_via.pack()

# Sonderansage Auswahl
var_special = tk.BooleanVar()
check_special = tk.Checkbutton(root, text="Sonderansage hinzufügen", variable=var_special)
check_special.pack()

combo_special = ttk.Combobox(root)
combo_special.pack()

# Liste der Sonderansagen automatisch laden
hinweis_pfad = os.path.join(BASE_PATH, "Hinweise")
if os.path.exists(hinweis_pfad):
    sonderdateien = [f for f in os.listdir(hinweis_pfad) if f.endswith(".mp3")]
    combo_special['values'] = sonderdateien

# Liste der Haltestellen automatisch laden
ziele_pfad = os.path.join(BASE_PATH, "Ziele")
if os.path.exists(ziele_pfad):
    haltestellen = [f[:-4] for f in os.listdir(ziele_pfad) if f.endswith(".mp3")]
    combo_destination['values'] = haltestellen
    combo_via['values'] = haltestellen

# Buttons
btn_generate = tk.Button(root, text="Ansage generieren und abspielen", command=generate_and_play)
btn_generate.pack(pady=10)

btn_special_only = tk.Button(root, text="Nur Sonderansage abspielen", command=play_special_only)
btn_special_only.pack(pady=5)

root.mainloop()
