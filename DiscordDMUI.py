# DiscordDMUI.py is the user interface for the DiscordDM module
# author: David Zhou
# version: 2.1
import os
from tkinter import *
import webbrowser
import threading
from queue import Queue
import time
import DiscordDMDataAccess
import DiscordDM
from pathlib import Path

class DiscordDMUI:
    accessor = None
    targets = None
    display = None
    
    def __init__(self):
        self.targets = []
        self.display = 0
        path = Path(os.getcwd() + "/data")
        if not os.path.exists(path):
            os.mkdir(path)
        path = Path(os.getcwd() + "/data/DiscordDM_DATA.json")
        self.accessor = DiscordDMDataAccess.DiscordDMAccessor(path)
        win = Tk()
        win.title("Discord Art Sender")
        #win.geometry('550x600')
        window = Frame(win)
        window.pack(side="top", expand=True, fill="both", padx=10, pady=10)
        window.pack_propagate(True) 
        self.MainPage(window)

        win.mainloop()

    def MainPage(self, window:Frame):
        rowpointer = 0

        editSource = Entry(window, width=25)
        editLinks = Entry(window, width=50)
        editTargetName = Entry(window, width=25)
        editTargetID = Entry(window, width=25)
        editAuth = Entry(window, width=50)

        Label(window, text="Enter Authentication: ").grid(column=0, row=rowpointer)
        editAuth.grid(column=1, row=rowpointer, columnspan=2)
        def changeAuth():
            self.accessor.setHeaders(editAuth.get())

        Button(window, text="Update", command=changeAuth).grid(column=3, row=rowpointer)
        rowpointer += 1

        Label(window, text="Message Source ID: ").grid(column=0, row=rowpointer)
        sourceID = Label(window, text=self.accessor.getSourceID())
        sourceID.grid(column=1, row=rowpointer)
        editSource.grid(column=2, row=rowpointer)

        def changeSource():
            self.accessor.setSource(editSource.get())
            sourceID.configure(text=self.accessor.getSourceID())

        Button(window, text="Update", command=changeSource).grid(column=3, row=rowpointer)
        rowpointer += 1

        Label(window, text="Searched Links: ").grid(column=0, row=rowpointer)

        links = self.accessor.getLinks()
        for entry in links:
            Label(window, text=entry, justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
            rowpointer += 1
        editLinks.grid(column=1, row=rowpointer, columnspan=2)

        def changeLink():
            change = editLinks.get()
            try:
                self.accessor.removeLink(change)
            except ValueError:
                self.accessor.addLink(change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                self.MainPage(window)

        Button(window, text="Add/Remove", command=changeLink).grid(column=3, row=rowpointer)
        rowpointer += 1

        Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
        self.targets = self.accessor.getTargets()
        for entry in self.targets:
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
                self.accessor.removeTarget(change)
            except ValueError:
                self.accessor.addTarget(change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                self.MainPage(window)
            
        Button(window, text="Add/Remove", command=changeTarget).grid(column=3, row=rowpointer)

        rowpointer += 1
        textNotice = "Any invalid data will be skipped when messages are sent"
        Label(window, text=textNotice,justify=LEFT).grid(sticky="w", column=0, row=rowpointer, columnspan=4)
        rowpointer += 1
        
        def toGroupPage():
            for widget in window.winfo_children():
                widget.destroy()
            self.GroupPage(window)
        def toManualSendPage():
            for widget in window.winfo_children():
                widget.destroy()
            self.ManualSendPage(window)
        def toAutoSendPage():
            for widget in window.winfo_children():
                widget.destroy()
            self.AutoSendPage(window)
        Button(window, text="View Groups", command=toGroupPage).grid(column=1, row=rowpointer)
        #Button(window, text="Manual Send", command=toManualSendPage).grid(column=2, row=rowpointer)
        Button(window, text="Automatic Send", command=toAutoSendPage).grid(column=3, row=rowpointer)


    def GroupPage(self, window:Frame):
        rowpointer = 0

        editMember = Entry(window, width=5)
        editGroup = Entry(window, width=15)

        Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
        half = len(self.targets)/2
        rowSub = rowpointer
        for i, entry in enumerate(self.targets):
            if i >= half:
                Label(window, text=f"**{i}** : " + entry["name"], justify=LEFT).grid(sticky="w", column=2, row=rowSub)
                rowSub += 1
            else:
                Label(window, text=f"**{i}** : " + entry["name"], justify=LEFT).grid(sticky="w", column=1, row=rowpointer)
                rowpointer += 1
        
        def toMainPage():
            for widget in window.winfo_children():
                widget.destroy()
            self.MainPage(window)

        Button(window, text="Return to main page", command=toMainPage).grid(column=1, row=rowpointer, columnspan = 2)
        rowpointer += 1

        groups = self.accessor.getGroups()
        groupKeys = list(groups.keys())
        try:
            Label(window, text=f"Members in \"{groupKeys[self.display]}\": ").grid(column=0, row=rowpointer)
            Label(window, text=f"group {self.display + 1}/{len(groupKeys)} ").grid(column=0, row=rowpointer + 1)
            group = groups[groupKeys[self.display]]
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
                change = self.targets[int(editMember.get())]
                try:
                    self.accessor.removeGroupMember(groupKeys[self.display], change)
                except ValueError:
                    self.accessor.addGroupMember(groupKeys[self.display], change)
                finally:
                    for widget in window.winfo_children():
                        widget.destroy()
                    self.GroupPage(window)

            Button(window, text="Add/Remove Member", command=changeMember).grid(column=2, row=rowpointer)
            rowpointer += 5
        except IndexError:
            pass

        def toNext():
            for widget in window.winfo_children():
                widget.destroy()
            self.display += 1
            self.GroupPage(window)
        def toPrev():
            for widget in window.winfo_children():
                widget.destroy()
            self.display -= 1
            self.GroupPage(window)

        if self.display - 1 >= 0:
            Button(window, text="Prev Group", command=toPrev).grid(column=0, row=rowpointer)
        if self.display + 1 < len(groupKeys):
            Button(window, text="Next Group", command=toNext).grid(column=1, row=rowpointer)

        def changeGroup():
            change = editGroup.get()
            try:
                self.accessor.removeGroup(change)
                if self.display == len(groupKeys) - 1:
                    self.display = 0
            except KeyError:
                self.accessor.addGroup(change)
            finally:
                for widget in window.winfo_children():
                    widget.destroy()
                self.GroupPage(window)

        editGroup.grid(column=2, row=rowpointer)
        Button(window, text="Add/Remove Group", command=changeGroup).grid(column=3, row=rowpointer)

    def ManualSendPage(self, window:Frame):
        rowpointer = 0
        artInfo = self.accessor.getContent()
        webbrowser.open(artInfo[0]["link"])
        editMember = Entry(window, width=5)
        editGroup = Entry(window, width=15)
        checkList = []
        Label(window, text = "Targetable Users: ").grid(column=0, row=rowpointer)
        for i, entry in enumerate(self.targets):
            checkList.append(Checkbutton(window, text=f"**{i}** : " + entry["name"], justify=LEFT))
        for entry in checkList:
            entry.grid(sticky="w", column=1, row=rowpointer)
            rowpointer += 1

    def ManualSend(self, checkList:list[Checkbutton]):
        global artInfo
        for i, entry in enumerate(checkList):
            if entry.get() == 1:
                for group in self.accessor.getGroups():
                    for member in group:
                        if member["name"] == self.targets[i]["name"]:
                            DiscordDM.Messenger(self.accessor.getHeader()).sendMsg(member["id"], {"content" : artInfo[0]["link"]})
                            break
        return -1

    def AutoSendPage(self, window:Frame):
        arts = self.accessor.getContent()
        groups = self.accessor.getGroups()
        header_params = self.accessor.getHeader()
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

        p = threading.Thread(target=self.messenger_task, args=(header_params, groups, arts, queue))
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
        if sendqueue.qsize() > 0:
            p = threading.Thread(target=self.messenger_task, args=(header_params, groups, arts, queue))
            p.start()
        text.insert(END, f" - : All process completed you may now close the window")
        text.see(END)


    def messenger_task(header_params:dict, groups:dict, arts:list, queue:Queue):
        try:
            mess = DiscordDM.Messenger(header_params)
            # DiscordDM.BulkMsg(groups, arts) but with queue logs
            for art in arts:
                try:
                    payload = {"content" : art["link"]}
                    
                    if art["sendGroup"].lower() not in groups:
                        queue.put(f"unknown:{art['link']}")
                        continue

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

                except Exception as e:
                    queue.put(f"error:{e}")
                    continue
                time.sleep(3)
                
        except Exception as e:
            queue.put(str(e))
        queue.put("done")
        return 1

    def sendTask(queue:Queue):
        order = queue.get()

    
