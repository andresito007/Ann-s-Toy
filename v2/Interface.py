import tkinter as tk
from tkinter import messagebox
import threading
import WordsGenerator as wg

class MainApplication:
    def __init__(self, parent):
        parent.title("Generator")
        self.frame = tk.Frame(parent)
        
        fontLabel = ("Helvetica", 16)
        colorLabel = "black"

        # Layout
        self.frame.grid_columnconfigure(0, minsize=25)
        self.frame.grid_columnconfigure(2, minsize=25)
        self.frame.grid_columnconfigure(5, minsize=25)
        self.frame.grid_columnconfigure(8, minsize=25)
        
        self.frame.grid_rowconfigure(0, minsize=25)
        self.frame.grid_rowconfigure(5, minsize=25)
        self.frame.grid_rowconfigure(7, minsize=25)

        # Labels
        text1 = "Grid settings"
        text2 = "Cols"
        text3 = "Rows"
        text4 = "Number of Objects"
        text5 = "Objects filename"
        text6 = "Show results"

        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text1).grid(column=1, row=1, sticky=tk.NW)
        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text2).grid(column=3, row=1, sticky=tk.NW)
        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text3).grid(column=6, row=1, sticky=tk.NW)
        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text4).grid(column=1, row=2, sticky=tk.NW)
        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text5).grid(column=1, row=3, sticky=tk.NW)
        tk.Label(self.frame, fg=colorLabel, font=fontLabel, text=text6).grid(column=1, row=4, sticky=tk.NW)

        # Entries Variables
        self.HorVar = tk.IntVar(self.frame, 3)
        self.VerVar = tk.IntVar(self.frame, 3)
        self.NumVar = tk.IntVar(self.frame, 8)
        self.FilVar = tk.StringVar(self.frame, "objects.txt")

        # Callbacks
        self.HorVar.trace("w", lambda name, index, mode, var = self.HorVar: self.CheckGridDimension(self.NumVar, self.HorVar, self.VerVar))
        self.VerVar.trace("w", lambda name, index, mode, var = self.VerVar: self.CheckGridDimension(self.NumVar, self.VerVar, self.HorVar))
        self.NumVar.trace("w", lambda name, index, mode, var = self.NumVar: self.CheckMaximumObjects(self.NumVar, self.HorVar, self.VerVar))

        # Entries
        tk.Entry(self.frame, font=fontLabel, justify="right", width=5, textvariable=self.HorVar).grid(column=4, row=1, sticky=tk.NW)
        tk.Entry(self.frame, font=fontLabel, justify="right", width=5, textvariable=self.VerVar).grid(column=7, row=1, sticky=tk.NW)
        tk.Entry(self.frame, font=fontLabel, justify="right", width=5, textvariable=self.NumVar).grid(column=4, row=2, sticky=tk.NW)
        tk.Entry(self.frame, font=fontLabel, justify="right", width=18, textvariable=self.FilVar).grid(column=4, row=3, sticky=tk.NW, columnspan=4)

        # CheckButton Variables
        self.showRes = tk.BooleanVar(self.frame, False)

        # CheckButton 
        tk.Checkbutton(self.frame, variable=self.showRes).grid(column=4, row=4, sticky=tk.W)

        # Buttons Variables
        buttonText1 = tk.StringVar(self.frame, "Generate")

        # Button
        tk.Button(self.frame, font=fontLabel, textvariable=buttonText1, command=self.GenerateWords).grid(column=3, row=6, sticky=tk.NW, columnspan=2)

        self.frame.pack()

    def CheckGridDimension(self, NumVar, IntVar, RemVar):
        try:
            intVar = IntVar.get()
            remVar = RemVar.get()
            numVar = NumVar.get()

            if intVar == "":
                pass 

            if intVar > 10:
                intVar = 10
            
            if intVar < 1:
                intVar = 1
        
            maximum = intVar*remVar

            if numVar < 1:
                numVar = 1

            if numVar > maximum:
                numVar = maximum

            IntVar.set(intVar)
            NumVar.set(numVar)
        except:
            pass
        
    def CheckMaximumObjects(self, NumVar, HorVar, VerVar):
        try:
            value = NumVar.get()
            maximum = HorVar.get() * VerVar.get()
            
            if value > maximum:
                NumVar.set(maximum)

            if value < 1:
                NumVar.set(1)
        except:
            pass

    def GenerateWords(self):
        self.thread = threading.Thread(target=self.ThreadProc)
        self.thread.start()

    def ThreadProc(self):
        cols = self.HorVar.get()
        rows = self.VerVar.get()
        nums = self.NumVar.get()
        file = self.FilVar.get()
        sRes = self.showRes.get()

        if not '.txt' in file:
            file = file + '.txt'

        shape = (cols, rows)
        shape = wg.CheckShape(shape)
        objs = wg.ReadObjs(shape, nums, file)
        for i, obj in enumerate(objs):
            im = wg.DrawGrid(shape)
            tilesDist = wg.ChooseTiles(shape, len(obj))
            wg.ScatterObjects(obj, tilesDist, im)

            if sRes:
                im.show()
            im.save(r'imgs\{}.png'.format(format(i, "03")))

        messagebox.showinfo("Info", "Process completed!")

def Main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()

if __name__ == '__main__':
    Main()