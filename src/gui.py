import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

title = "È un Gatto o un Cane?"
app_ver = "0.5"
authors = "Lucci Marco, Peshko Artur, Zucaro Simone"

root = tk.Tk()
root.resizable(0, 0)
root.geometry("900x900")
root.title(title + " v" + app_ver)
root.iconphoto(False, tk.PhotoImage(file ="img/logo.ico"))
root.columnconfigure(0, weight = 1)


# GUI Title
titleTxt = ttk.Label(
    root,
    text = title,
    font = ("Futura", 25, "bold")
)
titleTxt.grid(
    pady = (60, 60),
)

# Display img on the GUI
def addImg(source):
    img = Image.open(source)
    img = img.resize( (650, 450), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = ttk.Label(root,
                  image = img
                 )
    panel.grid(column = 0, row = 1, pady = (0, 15) )
    panel.image = img

addImg("img/placeholder1.png") # Init the img frame

# Selct the img from computer
def selectImg():
    file = fd.askopenfilename()
    addImg(file)
    ai_result("Cane")
    ai_percent("47%")

# Reset the img output
def clear():
    addImg("img/placeholder1.png")
    ai_result("Risultato")
    ai_percent("--%")

# Display the results
result_default = StringVar()
result_default.set("Risultato")
def ai_result(result):
    result_default.set(result)

# Display the percentage
perc_default = StringVar()
perc_default.set("--%")
def ai_percent(perc):
    perc_default.set(perc)

# Select Image button
select_button = ttk.Button(
    root,
    text = "Seleziona l'immagine",
    width = 35,
    command = selectImg
).grid(
    pady = (35, 10)
)

# Reset Image button
clear_button = ttk.Button(
    root,
    text = "Deseleziona l'immagine",
    width = 35,
    command = clear
).grid(
)

# Label for results
aiLabel = ttk.Label(
    root,
    textvariable = result_default,
    font = ("Futura", 14),
    width = 18
).grid(
    pady = (30, 0)
)

# Label for percentage
aiPercent = ttk.Label(
    root,
    textvariable = perc_default,
    font = ("Futura", 14),
    width = 18
).grid(
    pady = (0, 10)
)

# Credits label
creditsTxt = ttk.Label(
    root,
    text = title + " v" + app_ver + " - " + authors,
    font = ("Helvetica", 7),
    padding = 4
)
creditsTxt.grid(
    pady=82,
    sticky=E
)


root.mainloop()
