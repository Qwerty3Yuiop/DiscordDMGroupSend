# DiscordDMUI.py is the user interface for the DiscordDM module
# author: David Zhou
# version: 2.0
import os
from tkinter import *
import webbrowser
import threading
from queue import Queue
import time
import DiscordDMDataAccess
import DiscordDM


targets = []
display = 0
def MainPage(window:Frame):
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
            MainPage(window)

    Button(window, text="Add/Remove", command=changeLink).grid(column=3, row=rowpointer)
    rowpointer += 1

    Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
    targets = DiscordDMDataAccess.getTargets()
    for entry in targets:
        Label(window, text=entry["name"], justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
        w = Text(window, height=1, borderwidth=0, width=21)
        w.insert(1.0, entry["id"])
        w.grid(column=2, row=rowpointer)
        w.configure(state="disabled")
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
            MainPage(window)
        
    Button(window, text="Add/Remove", command=changeTarget).grid(column=3, row=rowpointer)

    rowpointer += 1
    textNotice = "Any invalid data will be skipped when messages are sent"
    Label(window, text=textNotice,justify=LEFT).grid(sticky="w", column=0, row=rowpointer, columnspan=4)
    rowpointer += 1
    
    def toGroupPage():
        for widget in window.winfo_children():
            widget.destroy()
        GroupPage(window)
    def toManualSendPage():
        for widget in window.winfo_children():
            widget.destroy()
        ManualSendPage(window)
    def toAutoSendPage():
        for widget in window.winfo_children():
            widget.destroy()
        AutoSendPage(window)
    Button(window, text="View Groups", command=toGroupPage).grid(column=1, row=rowpointer)
    #Button(window, text="Manual Send", command=toManualSendPage).grid(column=2, row=rowpointer)
    Button(window, text="Automatic Send", command=toAutoSendPage).grid(column=3, row=rowpointer)


def GroupPage(window:Frame):
    rowpointer = 0
    global targets
    global display

    editMember = Entry(window, width=5)
    editGroup = Entry(window, width=15)

    Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
    half = len(targets)/2
    rowSub = rowpointer
    for i, entry in enumerate(targets):
        if i >= half:
            Label(window, text=f"**{i}** : " + entry["name"], justify=LEFT).grid(sticky="w", column=2, row=rowSub)
            rowSub += 1
        else:
            Label(window, text=f"**{i}** : " + entry["name"], justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
            rowpointer += 1
    
    def toMainPage():
        for widget in window.winfo_children():
            widget.destroy()
        MainPage(window)

    Button(window, text="Return to main page", command=toMainPage).grid(column=1, row=rowpointer, columnspan = 2)
    rowpointer += 1

    groups = DiscordDMDataAccess.getGroups()
    groupKeys = list(groups.keys())
    try:
        Label(window, text=f"Members in \"{groupKeys[display]}\": ").grid(column=0, row=rowpointer)
        Label(window, text=f"group {display + 1}/{len(groupKeys)} ").grid(column=0, row=rowpointer + 1)
        group = groups[groupKeys[display]]
        for member in group:
            Label(window, text=member["name"], justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
            rowpointer += 1
        editMember.grid(column=1, row=rowpointer)
        feedback = Label(window, text="", justify=LEFT)
        feedback.grid(sticky="w", column=3, row=rowpointer)
        def changeMember():
            try:
                int(editMember.get())
            except Exception:
                feedback.configure(text="enter an integer value")
                return
            change = targets[int(editMember.get())]
            try:
                DiscordDMDataAccess.removeGroupMember(groupKeys[display], change)
            except ValueError:
                DiscordDMDataAccess.addGroupMember(groupKeys[display], change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                GroupPage(window)

        Button(window, text="Add/Remove Member", command=changeMember).grid(column=2, row=rowpointer)
        rowpointer += 5
    except IndexError:
        pass

    def toNext():
        global display
        for widget in window.winfo_children():
            widget.destroy()
        display += 1
        GroupPage(window)
    def toPrev():
        global display
        for widget in window.winfo_children():
            widget.destroy()
        display -= 1
        GroupPage(window)

    if display - 1 >= 0:
        Button(window, text="Prev Group", command=toPrev).grid(column=0, row=rowpointer)
    if display + 1 < len(groupKeys):
        Button(window, text="Next Group", command=toNext).grid(column=1, row=rowpointer)

    def changeGroup():
        global display
        change = editGroup.get()
        try:
            DiscordDMDataAccess.removeGroup(change)
            if display == len(groupKeys) - 1:
                display = 0
        except KeyError:
            DiscordDMDataAccess.addGroup(change)
        finally:
            for widget in window.winfo_children():
                widget.destroy()
            GroupPage(window)

    editGroup.grid(column=2, row=rowpointer)
    Button(window, text="Add/Remove Group", command=changeGroup).grid(column=3, row=rowpointer)

def ManualSendPage(window:Frame):
    rowpointer = 0
    global display
    global artInfo
    artInfo = DiscordDMDataAccess.getContent()
    webbrowser.open(artInfo[0]["link"])
    editMember = Entry(window, width=5)
    editGroup = Entry(window, width=15)
    checkList = []
    Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
    for i, entry in enumerate(targets):
        checkList.append(Checkbutton(window, text=f"**{i}** : " + entry["name"], justify=LEFT))
    for entry in checkList:
        entry.grid(sticky="w", column=1, row=rowpointer)
        rowpointer += 1

def ManualSend(checkList:list[Checkbutton]):
    global artInfo
    for i, entry in enumerate(checkList):
        if entry.get() == 1:
            for group in DiscordDMDataAccess.getGroups():
                for member in group:
                    if member["name"] == targets[i]["name"]:
                        DiscordDM.Messenger(DiscordDMDataAccess.getHeader()).sendMsg(member["id"], {"content" : artInfo[0]["link"]})
                        break
    return -1

def AutoSendPage(window:Frame):
    arts = DiscordDMDataAccess.getContent()
    groups = DiscordDMDataAccess.getGroups()
    header_params = DiscordDMDataAccess.getHeader()
    cycle = 0

    # cycle through symbols
    symbols = ["-", "\\", "|", "/"]

    # setup for scroll bar
    text = Text(window, wrap=WORD, height=12, width=80)
    logbar = Scrollbar(window, orient=VERTICAL, command=text.yview)
    text.configure(yscrollcommand=logbar.set)
    logbar.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Configure the Text widget for hyperlinks

    queue = Queue()
    sendqueue = Queue()

    p = threading.Thread(target=messenger_task, args=(header_params, groups, arts, sendqueue, queue))
    p.start()
    first = True
    while True:
        try:
            message = queue.get_nowait()
            first = True
            if str(message) == "done":
                break
            elif str(message).startswith("unknown:"):
                if "Waiting" in text.get("end-2c linestart", END):
                    text.delete("end-2c linestart", END)
                    text.insert(END, "\n")
                link = str(message).split(":")[1]
                text.insert(END, " - : Unknown entry queued for manual send")
                
            else:
                if "Waiting" in text.get("end-2c linestart", END):
                    text.delete("end-2c linestart", END)
                    text.insert(END, "\n")
                text.insert(END, f" - : {message}\n")
            
            queue.task_done()
            text.see(END)
        except Exception as e:
            if "Waiting" in text.get("end-2c linestart", END):
                text.delete("end-2c linestart", END)
                text.insert(END, "\n")
            text.insert(END, f" {symbols[cycle]} : Waiting... \n")
            if first:
                text.see(END)
            first = False

        cycle = (cycle + 1) % 4
        window.update()
        #time.sleep(.25)
    if "Waiting" in text.get("end-2c linestart", END):
        text.delete("end-2c linestart", END)
        text.insert(END, "\n")
    text.insert(END, " - : Finishing up...\n")
    queue.task_done()
    text.see(END)
    queue.join()
    p.join()

    text.insert(END, f" - : All process completed you may now close the window")
    text.see(END)


def messenger_task(header_params:dict, groups:dict, arts:list, sendqueue:Queue, queue:Queue):
    try:
        mess = DiscordDM.Messenger(header_params)
        # DiscordDM.BulkMsg(groups, arts) but with queue logs
        for art in arts:
            try:
                payload = {"content" : art["link"]}

                for user in groups[art["sendGroup"].lower()]:
                    response = mess.sendMsg(user["id"], payload)

                    while response == "<Response [429]>":
                        queue.put("Rate limited, waiting 5 seconds...")
                        time.sleep(5)
                        response = mess.sendMsg(user["id"], payload)
                    
                    if response != "<Response [200]>":
                        queue.put(f"An unknown response was received: {response}")
                        return
                    
                    queue.put(f"sent {art['link']} to {user['name']}")

            except Exception:
                queue.put(f"unknown:{art['link']}")
                continue
            time.sleep(3)
        while sendqueue.empty() == False:
            entry = sendqueue.get_nowait()
            queue.put(f"unknown:{entry}")
    except Exception as e:
        queue.put(str(e))
    queue.put("done")
    return 1



if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))
    DiscordDMDataAccess.initialize(path + "/data/DiscordDM_DATA.json")
    win = Tk()
    win.title("Discord Art Sender")
    #win.geometry('550x600')
    window = Frame(win)
    window.pack(side="top", expand=True, fill="both", padx=10, pady=10)
    window.pack_propagate(True) 
    MainPage(window)

    win.mainloop()
