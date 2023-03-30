from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack
from action import PaintStep
class UndoTracker:

    UndoStack : ArrayStack
    RedoStack : ArrayStack

    def __init__(self) -> None:
        self.UndoStack = ArrayStack(10000) #Assignment is always constant --> O(1)
        self.RedoStack = ArrayStack(10000) #Assignment is always constant --> O(1)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Args:
        - self
        - action = the PaintAction occuring 

        Raises:
        - Does not raise any erros

        Returns:
        - If the Undo Stack is full, return None
        - If it is not full, Do not return anything

        Complexity:
        - As all operations are of constant time, the best case will be equal to the worst case,
          therefore, best = worst = O(1)
        """
        if self.UndoStack.is_full(): #Integer comparison is always constant --> O(1)
            return None  #Returning is always constant --> O(1)
        else: #Integer comparison is always constant --> O(1)
            self.UndoStack.push(action) #Pushing is always constant --> O(1)

              
            

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        Args:
        - self
        - grid = The grid the undo was going to be applied on

        Raises:
        - Does not raise any errors

        Returns:
        - if the UndoStack is not empty, Returns the stack element the undo application was done in the form of a PaintAction
        - If UndoStack is empty, return None

        Complexity:
        - Best case will be if the stack is empty as it will simply require a return statement and therefore will be,
          best case = O(1). Worst case would be if the stack is not empty, in which then the run time would be,
          worst case = O(undo_apply) + O(k), where k represents the constant operations.
        """
        if self.UndoStack.is_empty(): #Integer comparison is always constant --> O(1)
            return None #Returning is always constant --> O(1)
        
        if not self.UndoStack.is_empty(): #Integer comparison is always constant --> O(1)
            UndoVariable = self.UndoStack.pop()#Popping is always constant --> O(1)
            self.RedoStack.push(UndoVariable) #Pushing is always constant --> O(1)
            UndoVariable.undo_apply(grid) #Will be of run time of --> O(undo_apply)
        return UndoVariable  #Returning is always constant --> O(1) 



    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        Args:
        - self
        - grid = The grid the undo was going to be applied on

        Raises:
        - Does not raise any errors

        Returns:
        - if the UndoStack is not empty, Returns the stack element the undo application was done in the form of a PaintAction
        - If UndoStack is empty, return None

        Complexity:
        - Best case will be if the stack is empty as it will simply require a return statement and therefore will be,
          best case = O(1). Worst case would be if the stack is not empty, in which then the run time would be,
          worst case = O(redo_apply) + O(k), where k represents the constant operations.
        
        """
        if self.RedoStack.is_empty():#Integer comparison is always constant --> O(1)
            return None #Returning is always constant --> O(1)

        if not self.RedoStack.is_empty(): #Integer comparison is always constant --> O(1)
            RedoVariable = self.RedoStack.pop() #Popping is always constant --> O(1)
            self.UndoStack.push(RedoVariable)  #Pushing is always constant --> O(1)
            RedoVariable.redo_apply(grid) #Will be of run time of --> O(redo_apply)
        return RedoVariable #Returning is always constant --> O(1)    
