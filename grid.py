from __future__ import annotations
from data_structures import referential_array
from layer_store import SetLayerStore

class Grid():
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style:str, x:int, y:int) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        
        self.draw_style_options = draw_style
        self.x = x
        self.y = y
        self.grid = Grid.MakeGrid(self,x,y)
        
        #raise NotImplementedError()

    
   

    
    
    
    
    
    #Grid method to make a grid based on class variables
    #O(n^2) due to the implentation of 2 for loops in order to create a two by two grid 
    def MakeGrid(self,x: int,y:int) -> list:
     GridArray = referential_array.ArrayR(x)
     for i in range(x):
        ListArray = referential_array.ArrayR(y)
        for j in range(y):
            ListArray[j]=SetLayerStore()
        GridArray[i] = ListArray
     return GridArray

    def increase_brush_size(self) -> int:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        
        #Inititliase brush size to 0
        while self.DEFAULT_BRUSH_SIZE < self.MAX_BRUSH:
            self.DEFAULT_BRUSH_SIZE+=1  #Increment brush size if it is less than maximum
            if self.DEFAULT_BRUSH_SIZE == self.MAX_BRUSH:
                break
        return self.DEFAULT_BRUSH_SIZE
        

    def decrease_brush_size(self) -> int:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        
        
        while self.DEFAULT_BRUSH_SIZE > self.MIN_BRUSH:
            self.DEFAULT_BRUSH_SIZE-= 1
            if self.DEFAULT_BRUSH_SIZE == self.MIN_BRUSH:
                break
        return self.DEFAULT_BRUSH_SIZE
    
    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for i in range(0,self.x):
            for j in range(0,self.y):
                self.grid[i][j].special()

    
    def __getitem__(self,x):
        return self.grid[x]