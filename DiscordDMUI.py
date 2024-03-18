from tkinter import *

targets = []

def main():
    window = Tk()
    window.title("Discord Art Sender")
    window.geometry('400x400')

    source = Label(window, text = "Art Source:")
    source.grid(column = 0, row = 0)

    sourceval = Label(window, text = "[insert source]")
    sourceval.grid(column = 1, row = 0)

    window.mainloop()

def displayTarg(screen):
    for target in targets:
        print("wow")
main()