from __future__ import annotations
from data_structures import referential_array
from layer_store import SetLayerStore
from layer_store import *

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
        
        self.draw_style = draw_style
        self.x = x
        self.y = y
        """
            Purpose:
            Makes the grid for further functionality

            Args:
            - x,y = dimensions of the grid 

            Raises:
            - If correct draw style is not implemented, then raise error: "Implement draw style"

            Returns:
            - No returning value 

            Complexity:

            - As shown above, both the loop runs for the their respective dimension times, as the variable x and y
             are representitive of the grid dimensions, the best case will always be equal to the worst case as the 
             grid function does not change depending on the value of x and y. As both the loops run for x and y times,
             the time complexity of the grid can be amounted by: O(x) * (y), if we are to group x and y as one variable 
             called dimension, it woud be represented as O(dimension) * O(dimension) which would equal to O(k*dimension^2 ) where k
             is some constant representing the assignment and checking below the for loops, therefore, replacing dimension with "n",
             the big O run time would be: O(k*n^2)
            """
        self.grid = referential_array.ArrayR(x)
        for i in range(x):
            self.grid[i] = referential_array.ArrayR(y) #Assignment is constant --> O(1)
        for i in range(x):   #Loop runs for x times 
            for j in range(y): #Loop runs for y times
                if self.draw_style == self.DRAW_STYLE_SET: #Checking is constant --> O(1)
                    self.grid[i][j]=SetLayerStore() # Assignment is constant --> O(1)
                elif self.draw_style == self.DRAW_STYLE_ADD: #Checking is constant --> O(1)
                    self.grid[i][j] = AdditiveLayerStore() #Assignment is constant --> O(1)
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE: #Checking is constant --> O(1)
                   self.grid[i][j] = SequenceLayerStore() #Assingment is constant --> O(1)
                else:
                    raise "Implement draw style"  # Time complexity not available      
            
        
  

    def increase_brush_size(self) -> int:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        
        Args:
        - self

        Raises:
        - Does not raise any errors

        Returns:
        - The changed brush size
        
        Complexity:
        - As we do not always know the default brush size, there are best and worst cases. Best case
          is if the default brush size is already equal to the brush size in which the while loop will 
          not need to increment "n" times, rather it will always stop at one size, therefore, Best Case = O(1).
          The worst case is if it needs to increment, in which it will increment "n" times so that the default 
          brush size is equal to the Maximum brush size, therefore, worst case = O(n)

        """
        while self.DEFAULT_BRUSH_SIZE < self.MAX_BRUSH: #Checking is constant time --> O(1)
            self.DEFAULT_BRUSH_SIZE+=1  #Increment brush size if it is less than maximum, Will increment an unknown amount --> O(comp==)
            if self.DEFAULT_BRUSH_SIZE == self.MAX_BRUSH: #Assignment is constant --> O(1)
                break #Time complexity is unavailable
        return self.DEFAULT_BRUSH_SIZE #Returning is always O(1)
        
        
        

    def decrease_brush_size(self) -> int:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Args:
        - self

        Raises:
        - Does not raise any errors

        Returns:
        - The changed brush size

        Complexity:
        - As we do not always know the default brush size, there are best and worst cases. Best case
          is if the default brush size is already equal to the brush size in which the while loop will 
          not need to decrement "n" times, rather it will always stop at one size, therefore, Best Case = O(1).
          The worst case is if it needs to decrement, in which it will increment "n" times so that the default 
          brush size is equal to the Minimum brush size, therefore, worst case = O(n)
        """
        while self.DEFAULT_BRUSH_SIZE > self.MIN_BRUSH:
            self.DEFAULT_BRUSH_SIZE-= 1
            if self.DEFAULT_BRUSH_SIZE == self.MIN_BRUSH:
                break
        return self.DEFAULT_BRUSH_SIZE
    
    def special(self):
        """
        Activate the special affect on all grid squares.

        Args:
        - self.x --> x dimension of the grid
        - self.y --> y dimension of the grid

        Raises:
        - Does not raise any errors

        Returns:
        - Does not return anything

        Complexity:
        - As there are two for loops implemented, each for loop will run x times and y times no matter
          circumstance, therefore, best case = worst case. As the two for loops will be run x times and 
          y times, the time complexity can be written as O(x) * O(y), re-writing both x and y as "n", we
          get O(n) * O(n) --> O(k*n^2 ) where k is a constant due to the recursive calling of special each time
        """
        for i in range(0,self.x): # Will run from 0 to x times
            for j in range(0,self.y): #Will run from 0 to y times
                self.grid[i][j].special() #O(1) as recursive function calling is constant

    
    def __getitem__(self,x):
        """
        Used to get an item from the invoked instances' attribute

        Args:
        - self
        - x
        
        Raises:
        - Does not raise an error
        
        Returns:
        - The grid of self.grid[x][y]

        Complexity:
        - Return statements are always O(1),therefore complexity is O(1)
        """
        return self.grid[x] #Return statements are alwyays constant --> O(1)