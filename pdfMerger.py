import os
from PyPDF2 import PdfFileMerger
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox

class Application(tk.Frame):
    listOfFilesToMerge = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    #todo clean layout
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

        #quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def addDocumentToList(self):
        filenames = tk.filedialog.askopenfilenames(initialdir = ".", title = "Select a File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*"))) 
        for file in filenames:
            #todo shorter filename
            self.listbox.insert("end", file)
            self.listOfFilesToMerge.append(file)

    def mergePdfs(self):
        if not self.listOfFilesToMerge:
            messagebox.showinfo("Title", "No pages to be merged") #TODO: disable btn if no files
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

root = tk.Tk()
root.geometry("500x300")
app = Application(master=root)
app.pack(fill=tk.BOTH, expand=True)
app.mainloop()