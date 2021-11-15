import tkinter as tk
import tkinter.font as font
from tkinter import Widget, ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from multiprocessing.pool import ThreadPool
from model import CATEGORIES, get_model, predict

title = "Cat or Dog"
app_ver = "0.7"
authors = "Lucci Marco, Peshko Artur, Zucaro Simone"
CATEGORIES = {
    "Dog": "Cane",
    "Cat": "Gatto",
}
pool = ThreadPool(processes=1)
model_async = pool.apply_async(get_model)

root = tk.Tk()
root.minsize(300, 550)
root.maxsize(600, 800)
root.title(f"{title} v{app_ver}")
root.iconphoto(False, tk.PhotoImage(file="logo.ico"))
root.columnconfigure(0, weight=1)


# GUI Title
titleTxt = ttk.Label(root, text=title, font=("Futura", 24, "bold"))
titleTxt.grid(pady=(10, 15))


# Display img on the GUI
def addImg(source):
    img = Image.open(source)
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = ttk.Label(root, image=img)
    panel.grid(column=0, row=1, padx=(10, 10))
    panel.image = img


addImg("empty.png")  # Init the img frame

# Selct the img from computer
def selectImg():
    file = fd.askopenfilename()
    addImg(file)
    model = model_async.get()
    prediction = predict(model, file)
    acc = prediction[1].cat if prediction[0] == "Cat" else prediction[1].dog
    ai_result(CATEGORIES[prediction[0]])
    ai_percent(acc)
    # TODO: get predictions from the model
    # ai_result("Cane")
    # ai_percent("47%")


# Reset the img output
def clear():
    addImg("empty.png")
    ai_result("Risultato")
    ai_percent("--%")


# Display the results
result_default = tk.StringVar()
result_default.set("Risultato")


def ai_result(result):
    result_default.set(result)


# Display the percentage
perc_default = tk.StringVar()
perc_default.set("--%")


def ai_percent(perc):
    perc_default.set(f"{perc*100: .2f}%")


# Select Image button
select_button = ttk.Button(root, text="Select Image", width=25, command=selectImg).grid(
    pady=(25, 3)
)

# Reset Image button
clear_button = ttk.Button(root, text="Clear", width=25, command=clear).grid()


# Label for results
aiLabel = ttk.Label(
    root, textvariable=result_default, font=("Futura", 18), width=12
).grid(pady=(20, 0))


# Label for percentage
aiPercent = ttk.Label(
    root, textvariable=perc_default, font=("Futura", 18), width=12
).grid(pady=(0, 10))


# Credits label
creditsTxt = ttk.Label(
    root,
    text=title + " v" + app_ver + " - " + authors,
    font=("Helvetica", 7),
    padding=4,
)
creditsTxt.grid(pady=(30, 0))


root.mainloop()
