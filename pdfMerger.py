import os
from PyPDF2 import PdfFileMerger
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #Button to merge all pdfs in current location
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Merge all pdfs at location:"+ os.getcwd()
        self.hi_there["command"] = self.mergePdfs
        self.hi_there.pack(side="top")

        #quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")


    def mergePdfs(self):
        pdfMerger = PdfFileMerger()

        #get list of all pdfs (TODO: make this a parameter for user to select which pdfs to add)
        listOfAllPDFs = []
        for file in os.listdir(os.getcwd()):
            if file.endswith(".pdf"):
                listOfAllPDFs.append(file)

        #merge all pdfs together
        for pdf in listOfAllPDFs:
            pdfMerger.append(open(pdf, 'rb'))

        #write the merged pdfs to a document with name result (TODO: name is parameter)
        with open("result.pdf", "wb") as fout:
            pdfMerger.write(fout)

root = tk.Tk()
app = Application(master=root)
app.mainloop()