# recipePicker.py
# Rajdeep Sandhu
# Python version: 3.12.5
import random
import sqlite3
import string
import tkinter as tk
import pyglet

from PIL import ImageTk


# From Tutorial: Create GUI App with Tkinter and SQLite
# https://www.youtube.com/watch?v=5qOnzF7RsNA
# Relational DB version


def fetch_db():
    with (sqlite3.connect("data/recipes.db") as conn):
        # connection = sqlite3.connect("data/recipes.db")
        cursor = conn.cursor()
        
        # Fetch all tables in the database schema
        query = """
        SELECT title, primary_key
        FROM recipes;
        """
        
        titles = cursor.execute(query).fetchall()
        # print(titles)
        idx = random.randint(0, len(titles) - 1)  # Random recipe
        
        # Fetch ingredients
        recipe_name = titles[idx][0]
        query = f"""
        SELECT name, qty, unit
        FROM  ingredients WHERE recipe_key=:k;
        """
        
        table_records = cursor.execute(query, {"k": idx}).fetchall()
        # print(recipe_name, '\n', table_records)
    
    return recipe_name, table_records


def pre_process(recipe_name, table_records):
    # title
    title = recipe_name
    
    # ingredients
    ingredients = []
    for i in table_records:
        name, qty, unit = i[0], i[1], i[2]
        if type(qty) == float:
            qty = int(qty)
            
        ingredients.append(" ".join(f"{qty} {unit} {name}".split()))
    
    return title, ingredients


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    
    # frame1 widgets: Logo
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")  # Load an image
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)  # Create a label widget using the image
    logo_widget.image = logo_img
    logo_widget.pack()
    
    # Instructions widget
    tk.Label(
            frame1,
            text="Ready for your random recipe?",
            font=("Shanti", 14),
            bg=bg_colour,
            fg="white"
            ).pack()
    
    # Button widget
    tk.Button(
            frame1,
            text="SHUFFLE",
            font=("Ubuntu", 20),
            bg="#28393a",
            fg="white",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: load_frame2()
            ).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    recipe_name, table_records = fetch_db()
    title, ingredients = pre_process(recipe_name, table_records)
    
    # frame2 widgets: Logo
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")  # Load an image
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)  # Create a label widget using the image
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
    # Title
    tk.Label(
            frame2,
            text=title,
            font=("Ubuntu", 20),
            bg=bg_colour,
            fg="white"
            ).pack(padx=25, pady=25)
    
    # Ingredients
    for i in ingredients:
        tk.Label(
                frame2,
                text=i,
                font=("Shanti", 12),
                bg="#28393a",
                fg="white"
                ).pack(padx=25, fill='both')
    
    # Back button
    tk.Button(
            frame2,
            text="BACK",
            font=("Ubuntu", 18),
            bg="#28393a",
            fg="white",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: load_frame1()
            ).pack(pady=20)


# initialise app
bg_colour = "#3d6466"
pyglet.font.add_file('fonts/Ubuntu-Bold.ttf')
pyglet.font.add_file('fonts/Shanti-Regular.ttf')

root = tk.Tk()
root.title("Recipe Picker")

# Window placement
root.eval("tk::PlaceWindow . center")  # Place the root window in the centre

# This is not the best method for placement
# x = root.winfo_screenwidth() // 2  # Get half the screen width
# y = int(root.winfo_screenheight() * 0.1)  # 10% of the screen height from the top
# root.geometry(f"500x600+{x}+{y}")

# Create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)  # Teal background
frame2 = tk.Frame(root, bg=bg_colour)  # Teal background

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nsew")

load_frame1()

# run app event loop
root.mainloop()
