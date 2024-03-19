import os
from tkinter import *
import DiscordDMDataAccess

targets = []

class mainPage:
    def __init__(self, window):
        global targets
        rowpointer = 0

        editSource = Entry(window, width=25)
        editLinks = Entry(window, width=50)
        editTargetName = Entry(window, width=25)
        editTargetID = Entry(window, width=25)

        Label(window, text="Message Source ID: ").grid(column=0, row=rowpointer)
        sourceID = Label(window, text=DiscordDMDataAccess.getSourceID())
        sourceID.grid(column=1, row=rowpointer)
        editSource.grid(column=2, row=rowpointer)

        def changeSource():
            DiscordDMDataAccess.setSource(editSource.get())
            sourceID.configure(text=DiscordDMDataAccess.getSourceID())

        Button(window, text="Update", command=changeSource).grid(column=3, row=rowpointer)
        rowpointer += 1

        Label(window, text="Searched Links: ").grid(column=0, row=rowpointer)

        links = DiscordDMDataAccess.getLinks()
        for entry in links:
            Label(window, text=entry, justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
            rowpointer += 1
        editLinks.grid(column=1, row=rowpointer, columnspan=2)

        def changeLink():
            change = editLinks.get()
            try:
                DiscordDMDataAccess.removeLink(change)
            except ValueError:
                DiscordDMDataAccess.addLink(change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                self = mainPage(window)

        Button(window, text="Add/Remove", command=changeLink).grid(column=3, row=rowpointer)
        rowpointer += 1

        Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
        targets = DiscordDMDataAccess.getTargets()
        for entry in targets:
            Label(window, text=entry["name"], justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
            Label(window, text=entry["id"], justify=RIGHT).grid(sticky="w", column=2, row=rowpointer)
            rowpointer += 1
        
        editTargetName.grid(column=1, row=rowpointer)
        editTargetID.grid(column=2, row=rowpointer)

        def changeTarget():
            change = {"name" : editTargetName.get(), "id" : editTargetID.get()}
            try:
                DiscordDMDataAccess.removeTarget(change)
            except ValueError:
                DiscordDMDataAccess.addTarget(change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                self = mainPage(window)
            
        Button(window, text="Add/Remove", command=changeTarget).grid(column=3, row=rowpointer)

        rowpointer += 1
        textNotice = "Any invalid data will be skipped when messages are sent"
        Label(window, text=textNotice,justify=LEFT).grid(sticky="w", column=0, row=rowpointer, columnspan=4)
        rowpointer += 1

        Button(window, text="View Groups", command=changeLink).grid(column=1, row=rowpointer)
        Button(window, text="Manual Send", command=changeLink).grid(column=2, row=rowpointer)
        Button(window, text="Automatic Send", command=changeLink).grid(column=3, row=rowpointer)



DiscordDMDataAccess.initialize(os.path.dirname(os.path.realpath(__file__)) + "\\data\\DiscordDM_DATA.json")
win = Tk()
win.title("Discord Art Sender")
win.geometry('550x600')
window = Frame(win)
window.pack(side="top", expand=True, fill="both")
page1 = mainPage(window)

win.mainloop()
