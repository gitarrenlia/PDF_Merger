import os
from PyPDF2 import PdfFileMerger
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from functools import partial
from directions import Directions

class Application(tk.Frame):
    listOfFilesToMerge = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    #todo clean layout
    #todo add buttons to change order of files
    #todo allow drag and drop of files
    def create_widgets(self):
        #Listbox with all documents from listOfFiles
        self.listbox = tk.Listbox(self)
        self.listbox.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)

        #Button to add document to list
        self.addBtn = tk.Button(self)
        self.addBtn["text"] = "Add document to be merged"
        self.addBtn["command"] = self.addDocumentToList
        self.addBtn.pack()

        #Button to merge all pdfs in current location
        self.mergeBtn = tk.Button(self)
        self.mergeBtn["text"] = "Merge all pdfs"
        self.mergeBtn["command"] = self.mergePdfs
        self.mergeBtn.pack(side="top")

        #Button up arrow
        self.upBtn = tk.Button(self)
        self.upBtn["text"] = "↑"
        self.upBtn["command"] = partial(self.moveElementInList, Directions.Up)
        self.upBtn.pack(side="right")

        #Button down arrow
        self.downBtn = tk.Button(self)
        self.downBtn["text"] ="↓"
        self.downBtn["command"] = partial(self.moveElementInList, Directions.Down)
        self.downBtn.pack(side="right")

        #quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    #adds documents from fileselector to the listbox and listOfFilesToMerge
    def addDocumentToList(self):
        filenames = tk.filedialog.askopenfilenames(initialdir = ".", title = "Select a File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*"))) 
        for file in filenames:
            self.listOfFilesToMerge.append(file)
        self.fillListboxFromList()

    #update listbox with elements from listOfFilesToMerge
    def fillListboxFromList(self):
        #todo shorter filename
        self.listbox.delete(0,tk.END)
        for file in self.listOfFilesToMerge:
            self.listbox.insert("end", file)

    def mergePdfs(self):
         #TODO: disable btn if no files
        if not self.listOfFilesToMerge:
            messagebox.showinfo("Title", "No pages to be merged")
            return
        resultfilename = tk.filedialog.asksaveasfilename(defaultextension=".pdf")
        pdfMerger = PdfFileMerger()

        #merge all pdfs together
        for pdf in self.listOfFilesToMerge:
            pdfMerger.append(open(pdf, 'rb'))

        #write the merged pdfs to a document with chosen name
        with open(resultfilename, "wb") as fout:
            pdfMerger.write(fout)

        messagebox.showinfo("Title", "Merged successfully")

    #change order of elements in list
    #if dir is enum Direction.Up the currently selected item in the listbox switches with the upper elemet
    #if dir is enum Direction.Down the selected item switches with the next element
    def moveElementInList(self, dir):
        picked = self.listbox.get(tk.ACTIVE)
        pickedIdx = self.listOfFilesToMerge.index(picked)
        if dir == Directions.Up:
            #todo instead disable btn
            if pickedIdx == 0:
                return
            self.listOfFilesToMerge[pickedIdx-1], self.listOfFilesToMerge[pickedIdx] = self.listOfFilesToMerge[pickedIdx], self.listOfFilesToMerge[pickedIdx-1]
            self.fillListboxFromList()
        elif dir == Directions.Down:
            #todo instead disable btn
            if pickedIdx == len(self.listOfFilesToMerge)-1:
                return
            self.listOfFilesToMerge[pickedIdx+1], self.listOfFilesToMerge[pickedIdx] = self.listOfFilesToMerge[pickedIdx], self.listOfFilesToMerge[pickedIdx+1]
            self.fillListboxFromList()

root = tk.Tk()
root.geometry("500x300")
app = Application(master=root)
app.pack(fill=tk.BOTH, expand=True)
app.mainloop()