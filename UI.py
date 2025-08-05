import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

root = tk.Tk()
root.title("Plant Doctor")
root.configure(bg="black")
root.geometry("700x800")

# Logo
logo_path = r"E:\SNS IT\project\plant_doctor\image\logo.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((180, 200))
logo = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(root, image=logo, bg="black")
logo_label.pack(pady=(50, 30))

# Fonts
font_label = ("Arial", 13)
font_entry = ("Arial", 12)

form_frame = tk.Frame(root, bg="black")
form_frame.pack(pady=10)

entries = []

def add_label_entry(parent, text):
    label = tk.Label(parent, text=text, fg="white", bg="black", font=font_label, anchor="w")
    entry = tk.Entry(parent, width=45, font=font_entry)
    label.pack(anchor="w", padx=30, pady=(8, 2))
    entry.pack(padx=30, pady=(0, 6))
    entries.append(entry)
    return entry

flower_name_entry = add_label_entry(form_frame, "Name of the Flower:")
plant_color_entry = add_label_entry(form_frame, "Plant Color:")
plant_age_entry = add_label_entry(form_frame, "Age of the Plant (seedling, mature, etc.):")
soil_type_entry = add_label_entry(form_frame, "Soil Type:")
mature_level_entry = add_label_entry(form_frame, "Mature Level:")

patches_label = tk.Label(form_frame, text="Any Patches:", fg="white", bg="black", font=font_label, anchor="w")
patches_label.pack(anchor="w", padx=30, pady=(10, 2))

patches_var = tk.StringVar(value="No")
patches_frame = tk.Frame(form_frame, bg="black")
patches_frame.pack(padx=30, pady=(0, 10))

yes_radio = tk.Radiobutton(patches_frame, text="Yes", variable=patches_var, value="Yes", bg="black", fg="white", font=font_entry, selectcolor="black")
no_radio = tk.Radiobutton(patches_frame, text="No", variable=patches_var, value="No", bg="black", fg="white", font=font_entry, selectcolor="black")
yes_radio.pack(side="left", padx=10)
no_radio.pack(side="left", padx=10)

# Info Frame for Results
info_frame = tk.Frame(root, bg="black")
info_box = tk.Text(
    info_frame,
    bg="white",
    font=font_entry,
    wrap="word",
    relief="solid",
    bd=2,
    height=1,
    width=65  # Fixed width to avoid expanding sideways
)
info_box.config(state='disabled')

def back_to_lobby():
    info_frame.pack_forget()
    form_frame.pack(pady=10)
    submit_btn.pack(pady=20)

back_button = tk.Button(
    info_frame,
    text="Back to Lobby",
    command=back_to_lobby,
    font=("Arial", 12, "bold"),
    bg="gray",
    fg="white",
    width=20
)

def submit_form():
    form_frame.pack_forget()
    submit_btn.pack_forget()

    # Fetch the values from the entry fields and remove leading/trailing spaces
    flower = flower_name_entry.get().strip()  # .strip() will remove extra spaces or tabs
    color = plant_color_entry.get().strip()
    age = plant_age_entry.get().strip()
    soil = soil_type_entry.get().strip()
    mature = mature_level_entry.get().strip()
    patches = patches_var.get().strip()

    try:
        result = subprocess.run(
            ["python", r"E:\SNS IT\project\plant_doctor\main.py", flower, color, age, soil, mature, patches],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        output_text = result.stdout.strip() if result.stdout else "No output from backend."
    except subprocess.CalledProcessError as e:
        output_text = f"[Error Running Backend]\n{e.stderr}"
    except Exception as e:
        output_text = f"Unexpected Error:\n{str(e)}"

    info_box.config(state='normal')
    info_box.delete("1.0", tk.END)
    info_box.insert(tk.END, output_text)

    # Colorful highlights
    for tag, color in [("✅", "green"), ("⚠️", "orange"), ("❌", "red"), ("🌸", "purple"), ("💧", "blue"), ("☀️", "gold")]:
        start = "1.0"
        while True:
            pos = info_box.search(tag, start, stopindex=tk.END)
            if not pos:
                break
            end = f"{pos}+{len(tag)}c"
            info_box.tag_add(tag, pos, end)
            info_box.tag_config(tag, foreground=color)
            start = end

    info_box.config(state='disabled')
    info_box.update_idletasks()
    lines = int(info_box.index('end-1c').split('.')[0])
    info_box.config(height=lines + 2)

    info_frame.pack(pady=30)
    info_box.pack(pady=10, padx=40, anchor="center")
    back_button.pack(pady=10)

submit_btn = tk.Button(root, text="Submit", bg="blue", fg="white", font=("Arial", 14, "bold"), width=20, command=submit_form)
submit_btn.pack(pady=20)

# Enter key navigation
def focus_next(event, idx):
    if idx + 1 < len(entries):
        entries[idx + 1].focus()
    else:
        yes_radio.focus()

for i, entry in enumerate(entries):
    entry.bind("<Return>", lambda e, idx=i: focus_next(e, idx))

# Start
root.mainloop()
