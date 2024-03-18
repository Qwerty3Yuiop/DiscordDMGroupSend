from tkinter import *
import DiscordDMDataAccess

targets = []

def main():
    DiscordDMDataAccess.initialize("./data/DiscordDM_DATA.json")

    window = Tk()
    window.title("Discord Art Sender")
    window.geometry('400x400')

    source = Label(window, text = "Art Source:")
    source.grid(column = 0, row = 0)

    sourceval = Label(window, text = "[insert source]")
    sourceval.grid(column = 1, row = 0)

    links = DiscordDMDataAccess.getLinks()
    print(links)
    for count, entry in enumerate(links):
        print(count, ": ", entry)
        Label(window, text = entry, justify=LEFT).grid(sticky = "w", column = 0, row = count + 2)     
    window.mainloop()

def displayTarg(screen):
    for target in targets:
        print("wow")
main()