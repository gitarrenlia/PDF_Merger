import os
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from functools import partial
from directions import Directions
from tkinter import ttk

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

        #treeview with all files from listOfFilesToMerge
        self.tree = ttk.Treeview(root, columns=('#1', '#2'), show='headings', selectmode='browse')
        self.tree.heading('#1', text='Pages')
        self.tree.heading('#2', text='Filename')
        self.tree.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)

        #Button to add document to list
        self.addBtn = tk.Button(self)
        self.addBtn["text"] = "Add document to be merged"
        self.addBtn["command"] = self.addDocumentToList
        self.addBtn.pack(side="left")

        #Button to merge all pdfs in current location
        self.mergeBtn = tk.Button(self)
        self.mergeBtn["text"] = "Merge all pdfs"
        self.mergeBtn["command"] = self.mergePdfs
        self.mergeBtn.pack(side="bottom")

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

    #adds documents from fileselector to the listbox and listOfFilesToMerge
    def addDocumentToList(self):
        filenames = tk.filedialog.askopenfilenames(initialdir = ".", title = "Select a File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*"))) 
        for file in filenames:
            self.listOfFilesToMerge.append(file)
        self.fillTreeFromList()

    #update listbox with elements from listOfFilesToMerge
    def fillTreeFromList(self):
        #todo shorter filename
        self.tree.delete(*self.tree.get_children())#delete all children (*-splat/unpack-operator produces the individual elemtents of the iterable)
        for file in self.listOfFilesToMerge:
            with open(file, "rb") as pdf_file:
                head, tail = os.path.split(file)
                pdf_reader = PdfFileReader(pdf_file)
                self.tree.insert('', tk.END, values=(pdf_reader.numPages,tail))

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
        pickedIdx = self.tree.index(self.tree.selection())
        if dir == Directions.Up:
            #todo instead disable btn
            if pickedIdx == 0:
                return
            self.listOfFilesToMerge[pickedIdx-1], self.listOfFilesToMerge[pickedIdx] = self.listOfFilesToMerge[pickedIdx], self.listOfFilesToMerge[pickedIdx-1]
            self.fillTreeFromList()
            self.tree.selection_set(self.tree.get_children()[pickedIdx-1]) 
        elif dir == Directions.Down:
            #todo instead disable btn
            if pickedIdx == len(self.listOfFilesToMerge)-1:
                return
            self.listOfFilesToMerge[pickedIdx+1], self.listOfFilesToMerge[pickedIdx] = self.listOfFilesToMerge[pickedIdx], self.listOfFilesToMerge[pickedIdx+1]
            self.fillTreeFromList()
            self.tree.selection_set(self.tree.get_children()[pickedIdx+1]) 



root = tk.Tk()
root.geometry("500x300")
app = Application(master=root)
app.pack(fill=tk.BOTH, expand=True)
app.mainloop()