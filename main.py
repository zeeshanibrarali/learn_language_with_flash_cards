from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original = pandas.read_csv("data/french_words.csv")
    to_learn = original.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    
def next_card():
    global current_card, flip
    window.after_cancel(flip)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill= "black")
    canvas.itemconfig(word, text=current_card["French"], fill= "black")
    canvas.itemconfig(background, image=front_image)
    flip = window.after(3000, func = flip_card)

def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(background, image=back_image)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Zee flash")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip = window.after(3000, func = flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
background = canvas.create_image(400, 263, image=front_image)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()