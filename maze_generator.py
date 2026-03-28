import tkinter as tk 

class Maze:
    def __init__(self, rows=20,cols=20):
        self.rows = rows
        self.cols = cols

        self.grid = [[{'N','S','E','W'} for _ in range(cols)] for _ in range(rows)]

        
        self.pathdict = {
            "N" : (-1,0,"S"),
            "S" : (1,0,"N"),
            "E" : (0,1,"W"),
            "W" : (0,-1,"E"),
        }    


class MazeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("@astaffz Maze Generator")
        self.geometry("500x500")
        self.configure(bg="black")




if __name__ == "__main__":
    mv = MazeView()
    mv.mainloop()