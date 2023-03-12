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
     MAX_CAPACITY = x*y
     GridArray = referential_array.ArrayR(MAX_CAPACITY)
     for i in range(x):
        ListArray = referential_array.ArrayR(x)
        for j in range(y):
            ListArray[j]=SetLayerStore(x,y,(255,255,255))
        GridArray[i] = ListArray
     return GridArray

    def increase_brush_size(self) -> int:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        MAX_BRUSH = 5
        brush_size = 0 #Inititliase brush size to 0
        while brush_size < MAX_BRUSH:
            brush_size+=1  #Increment brush size if it is less than maximum
            if brush_size == MAX_BRUSH:
                break
        return brush_size
        

    def decrease_brush_size(self) -> int:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        MIN_BRUSH = 0
        brush_size = 0
        while brush_size > MIN_BRUSH:
            brush_size-=1
            if brush_size == MIN_BRUSH:
                break
        return brush_size  
    
    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for element in self.grid:
            for i in element:
                self.special()

    
    def __getitem__(self,x):
        return self.grid[x]