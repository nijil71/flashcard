import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data_dict = {}
try:
    data = pandas.read_csv("data/to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient='records')
else:
    data_dict = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(language_words, text=current_card['French'], fill="black")
    canvas.itemconfig(canvas_image, image=photo_front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(language_words, text=current_card['English'], fill="white")
    canvas.itemconfig(canvas_image, image=photo_back)


def known():
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/to_learn.csv", index=False)
    next_card()


# User Interface
window = Tk()
window.title("Flash Card")
window.configure(background=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
photo_front = PhotoImage(file="images/card_front.png")
photo_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 270, image=photo_front, anchor=CENTER)

language = canvas.create_text(400, 150, text="", font=("Ariel", 40, 'italic'), fill="black", anchor=CENTER)
language_words = canvas.create_text(400, 263, text="", font=("Ariel", 60, 'bold'), fill="black", anchor=CENTER)
canvas.grid(row=0, column=1, columnspan=2, pady=50, padx=50)
unknown_image = PhotoImage(file="images/wrong.png")
unknown_word = Button(window, image=unknown_image, highlightthickness=0, border=0, command=next_card)
unknown_word.grid(row=1, column=1, pady=(0, 50))
known_image = PhotoImage(file="images/right.png")
known_word = Button(window, image=known_image, highlightthickness=0, border=0, command=known)
known_word.grid(row=1, column=2, pady=(0, 50))
next_card()

window.mainloop()
