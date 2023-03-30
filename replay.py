from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from action import PaintAction

class ReplayTracker:

    
    ReplayQueue : CircularQueue


    def __init__(self) -> None:
        self.ReplayQueue = CircularQueue(10000) #Assignment is always constant


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args:
        - action = The paintAction being implemented
        - is_undo = Boolean for keeping track of if undo is called or not

        Raises:
        - Does not raise any errors

        Returns:
        - Does not return anything 

        Complexity:
        - As all operations are constant, best case = worst case  = O(1)
        """
        
        if not self.ReplayQueue.is_full(): #Integer comparison is always constant --> O(1)
            self.ReplayQueue.append((action,is_undo))  #Appending for circular queues is always constant --> O(1)
            
   

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Args:
        - self
        - grid = The grid the undo was going to be applied on    

        Raises:
        - Does not raise any errors

        Returns:
        - If ReplayQueue is empty, return True
        - If ReplayQueue is not empty, return False

        Complexity:
        - As all operations are constant except of those that are of redo_apply and undo_apply,
          it is safe to assume that best case = worst case. If redo apply is called, then the 
          run time complexity is equal to O(k) + O(redo_apply) where k is an integer which represents
          the constant operations. If Undo apply is called, then the 
          run time complexity is equal to O(k) + O(undo_apply) where k is an integer which represents
          the constant operations.
        """
        if not self.ReplayQueue.is_empty(): #Integer comparison is always constant --> O(1)
            ActionReplay = self.ReplayQueue.serve()  # Serving circular queue is always constant --> O(1)
            if ActionReplay[1] == False: #Integer comparison is always constant --> O(1)
                ActionReplay[0].redo_apply(grid) #Will be of run time of --> O(redo_apply)
            else: #Integer comparison is always constant --> O(1)
                ActionReplay[0].undo_apply(grid) #Will be of run time of --> O(undo_apply)
            return False #Returning is always constant --> O(1) 
        else: #Integer comparison is always constant --> O(1)
            return True  #Returning is always constant --> O(1)    



       


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

