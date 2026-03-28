import tkinter as tk 
import random
import argparse

VERSION = "1.1"

class Maze:
    def __init__(self, rows=20,cols=20):
        self.rows = rows
        self.cols = cols

        self.grid = []

        """
        A dictionary that translates the algorithm's current output
        into (row-delta, column-delta, opposite wall)
        """
        self.pathdict = {
            "N" : (-1,0,"S"),
            "S" : (1,0,"N"),
            "E" : (0,1,"W"),
            "W" : (0,-1,"E"),
        }    

     
    def _isInBounds(self,row,col):
        return row >= 0 and col >= 0 and row < self.rows and col < self.cols
    
    def _appendValidWalls(self,walls,cell_row, cell_col):
        for direct, (row_delta, col_delta, _) in self.pathdict.items():
            if self._isInBounds(cell_row+row_delta,cell_col+col_delta):
                walls.append((cell_row,cell_col,direct))

    def generate(self):
        self.grid = [[{'N','S','E','W'} for _ in range(self.cols)] for _ in range(self.rows)]
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        start_r, start_c = (random.randrange(self.rows), random.randrange(self.cols))
        visited[start_r][start_c] = True
        '''
         walls is a list of tuples (row, column, direction)
         indicating that the cell at [row][column] has a valid wall 
         in the specificed direction
        '''
        walls = []
        self._appendValidWalls(walls, start_r,start_c)

        while walls:
             # Pick a random wall
            wallToRemove = random.randrange(len(walls))
            # Swap with the last wall in the list. Lists are an array of pointers in python, making this is O(1) behaviour.
            walls[wallToRemove],walls[-1] = walls[-1],walls[wallToRemove]

            curr_cell_r, curr_cell_c, wall_from_cell = walls.pop()
            row_delta, column_delta, wall_from_neighbor = self.pathdict[wall_from_cell]
            neighbor_r,neighbor_c = curr_cell_r+row_delta, curr_cell_c+column_delta
            
            if not visited[neighbor_r][neighbor_c]:
                visited[neighbor_r][neighbor_c] = True
                self.grid[curr_cell_r][curr_cell_c].discard(wall_from_cell)
                self.grid[neighbor_r][neighbor_c].discard(wall_from_neighbor)

                self._appendValidWalls(walls,neighbor_r,neighbor_c)
        self.grid[0][0].discard("N")
        self.grid[self.rows - 1][self.cols - 1].discard("S")

class MazeView(tk.Tk):

    def _get_grid_size(self):
        return int(min(
    self.canvas.winfo_width() * (self.MAZE_WINDOW_COVERAGE_PCT / 100) / self.maze.cols,
    self.canvas.winfo_height() * (self.MAZE_WINDOW_COVERAGE_PCT / 100) / self.maze.rows
))
    

    def _draw_maze(self):
        self.canvas.delete("all")
        size = self._get_grid_size()
        maze_w = size * self.maze.cols
        maze_h = size * self.maze.rows
        offset_x = (self.canvas.winfo_width() - maze_w) // 2
        offset_y = (self.canvas.winfo_height() - maze_h) // 2
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                x = offset_x + c*size
                y = offset_y + r*size
                for wall in self.maze.grid[r][c]:
                    if wall == "N":
                        self.canvas.create_line(x,y,x+size,y, fill="green",width=2)
                    elif wall == "S":
                        self.canvas.create_line(x,y+size,x+size,y+size, fill="green",width=2)
                    elif wall == "E":
                        self.canvas.create_line(x+size,y,x+size,y+size, fill="green",width=2)
                    elif wall == "W":
                        self.canvas.create_line(x,y,x,y+size, fill="green",width=2)

    def _on_resize(self,event):
        if self._resize_job != None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(100,self._draw_maze)

    def __init__(self,rows,cols,coverage):
        super().__init__()
        self.title("@astaffz Maze Generator")
        self.geometry("500x500")
        self.configure(bg="black")
        self.MAZE_WINDOW_COVERAGE_PCT = coverage
        self.maze = Maze(rows,cols)
        self.maze.generate()
        
        self._resize_job = None
        self.canvas = tk.Canvas(self,width=500,height=500,bg="black")
        self.canvas.pack(fill=tk.BOTH,expand=True)
        self.canvas.bind("<Configure>",self._on_resize)




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description=f"A script that generates a random solvable maze using Prim's algorithm.\nVersion {VERSION} by Aid M. (@astaffz)")
    parser.add_argument("--rows", type=int, default=20, help="Define the number of rows (default is 20)")
    parser.add_argument("--cols", type=int, default=20, help="Define the number of columns (default is 20)")
    parser.add_argument("--maze-window-percentage",type=int,default=85, help="Define the percentage of the frame covered by the maze.")
    cli_args = parser.parse_args()

    mv = MazeView(cli_args.rows,cli_args.cols,cli_args.maze_window_percentage)
    mv.mainloop()
