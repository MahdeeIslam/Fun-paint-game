from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import ArrayStack
from layers import invert
from data_structures.queue_adt import CircularQueue
from data_structures.queue_adt import Queue
from data_structures.sorted_list_adt import SortedList
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from layers import *
from layer_util import get_layers

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        

        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    MAX_CAPACITY = 1 #Constant --> O(1)
    
    
    def __init__(self) -> None:
        self.LayerApplied = ArrayStack(self.MAX_CAPACITY) #Assignment is constant --> O(1)
        self.flag = False #Assignment is constant --> O(1)
        
    
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Args:
        - self
        - layer --> layer we want to add

        Raises:
        - Does not raise an error

        Returns:
        - Returns a Boolean depending on the length of the stack
        - If length of stack < Maximum capacity of the stack, then return True
        - If length of stack >= Maximum capacity of the stack, then return False

        Complexity:
        - All elements of the function is constant except for the clear, in terms of best 
          case scenerio, if the length of the LayerApplied stack is indeed less then the
          maximum capacity, then the clear function is not called and therefore, the 
          best case = O(1). The worst case is the length of the LayerApplied stack is 
          equal to or greater than the maximum capacity as that will need to call the 
          clear function which needs clear "n" times making the worst case = O(k*n) where
          k is a constant due to the other constant implementations
        """
        
        if len(self.LayerApplied) < self.MAX_CAPACITY: #Checking is constant --> O(1)
            self.LayerApplied.push(layer) #Pushing is always constant --> O(1) 
            return True #Return Statement always constant --> O(1)
        else:
            self.LayerApplied.clear() #Clearing is linear time depending on the amount of elements in the stack --> O(n)
            self.LayerApplied.push(layer) #Pushing is always constant --> O(1)
        return False #Returning is always constant --> O(1)
             

    
    def get_color(self,start: tuple ,timestamp: float, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - self
        - Start = The starting colour provided and it is a tuple
        - timestamp = Used by some layers for dynamic effects and it is a float
        - x = x dimensions of the grid and it is an integer
        - y = y dimensions of the grid and it is an integer

        Raises:
        - Does not raise any value errors

        Returns:
        - If special (flag) is not called and the stack is not empty, it will return the effected color tuple
        - If special (flag) is not called and the stack is empty, it will return the original color tuple
        - If special (flag) is called and the stack is not empty, it will return the effected color tuple
        - If special (flag) is called and the stack is empty, it will simply return the inverted layer application

        Complexity:
        - If special (flag) is not called, the best case time complexity is if the stack is empty as it wil require simply 
          just a return statement of the original color tuple which is of constant run time, therefore,
          best case if special is not called  = O(1). The worst case is if the the stack already has elements inside in
          which apply function must be called, therefore, the worst case = O(apply) + O(k) where k is some constant for the 
          other operations therefore being O(apply + k).
        
        - If special (flag) is called, the best case will be equal to the worst case as they both involve applying to the LayerStore,
          therefore, best = worst. If the stack is empty, then the runtime will simply be O(apply). If the stack is not empty, the runtime
          will simply be O(apply + k), where k is some constant representing the other operations. As the input size goes to infinity, the 
          adding constant will not cause a significant change to the run time therefore both run time are O(apply) = O(apply) = best = worst

        """
        if not self.flag: #Assignment is constant --> O(1)
            if not self.LayerApplied.is_empty(): #Integer comparison is always constant --> O(1)
                LayerEffect = self.LayerApplied.peek() #Peeking is always constant --> O(1)
                start = LayerEffect.apply(start,timestamp,x,y) # Apply takes the run time of --> O(apply)
                return start # Returnig is always constant --> O(1)
            if self.LayerApplied.is_empty(): #Integer comparison is always constant --> O(``)
                return start #Returning is always constant
        else:
            if self.LayerApplied.is_empty(): #Integer comparison is always constant
                return invert.apply(start,timestamp,x,y) # Apply takes the run time of O(apply)
           
            if not self.LayerApplied.is_empty(): #Integer comparison is always constant --> O(1)
                LayerEffect = self.LayerApplied.peek() #Peeking is always constant --> O(1)
                start = LayerEffect.apply(start,timestamp,x,y) #Apply has the run time of --> O(apply)
                start = (255-start[0],255-start[1],255-start[2]) # Constant run time as integer setting is always constant --> O(1)
        return start #Returning is always constant --> O(1)
          
        
       
    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Args:
        - layer = layer that will be erased
        - self

        Raises;
        - Does not raise any errors

        Returns:
        - If the stack is empty, LayerStore was not changed, therefore, returns false
        - If the stack is not empty, LayerStore was changed, therefore, returns true

        Complexity:
        - As all operations for erase are of constant run time, the best case will be equal to the worst
          case, therefore being best case = worst case = O(1)
        """
        if self.LayerApplied.is_empty(): #Integer comparison is always constant --> O(1)
            return False #Returning is always constant --> O(1)
        else:
            self.LayerApplied.pop() #Popping is always constant --> O(1)
            return True #Returning is always constant --> O(1)

      

    def special(self):
        """
        Special mode. Different for each store implementation.

        Args:
        - self

        Raises:
        - Does not raise any errors

        Returns:
        - Does not return anything

        Complexity:
        - Comparison is always constant, therefore best case = worst case = O(1)
        """
        self.flag = not self.flag #Comparison is always constant --> O(1)
        
            
        
        

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    MAX_CAPACITY = 100 #Constant --> O(1)

    def __init__(self) -> None:
        self.AppliedLayer = CircularQueue(self.MAX_CAPACITY) #Constant --> O(1)
        self.size = 0 #Constant --> O(1)
        
        
    
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Args:
        - layer = Layer which will be added
        - self

        Raises:
        - If queue is full, raise an error: "Queue is full" 

        Returns:
        - Returns True if the Circular queue is not full, if queue is full, queue will raise an error.

        Complexity:
        - If the queue is not full, then all operations are constant, therefore the best case is equal to the worst case
          being best = worst = O(1).
        - If the queue is full, it will simply raise an error in which raisng time complexity cannot be measured
        - Therefore, best case = worst case = O(1)
        """

        if not self.AppliedLayer.is_full(): #Checking if it is full, integer comparison is always constant --> O(1)
            self.AppliedLayer.append(layer) #Appending for circular queues is always constant --> O(1)
            self.size += 1 #increments the known size by 1, only done once, therefore being constant --> O(1)
            return True #Returning statements is always constant --> O(1)
        else: # Integer comparison is always constant 
            raise "Queue is full"  #No time complexity for raising   
    
    def get_color(self, start: tuple, timestamp: float, x: int , y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - self
        - start = Starting color provided and it is a tuple
        - timestamp = Used by some layers for dynamic effects and it is a float
        - x = x dimensions of the grid and it is an integer
        - y = y dimensions of the grid and it is an integer

        Raises:
        - Does not raise any errors

        Returns:
        - If the queue is empty, simply return the starting color tuple
        - If the queue is not empty, it will return the effected color

        Complexity:
        - For the entire function, the best case is if the queue is empty as it will simply return the 
          starting color tuple, all being constant time, therefore, the best case = O(1). The worst case is 
          if the queue is not empty, it will run for a total of size times to get the color and apply to the 
          LayerStore. Therefore, the worst case = O(self.size) + O(apply) + O(1) = O(self.size + apply + k) where k 
          is a constant representing the constant operations. As the input size increases to infinty, the constant will
          not play a major role in the time complexity affection. Therefore, worst case = O(self.size + apply)
        """
        
        if self.AppliedLayer.is_empty(): #Integer comparison is always constant --> O(1)
            return start #Returning is always constant --> O(1)
           
        for i in range(self.size): # Will run for self. size times
            if not self.AppliedLayer.is_empty(): #Integer comparison is always constant --> O(1)
                LayerEffect = self.AppliedLayer.serve() # Serving circular queue is always constant --> O(1) 
                start = LayerEffect.apply(start,timestamp,x,y) #Applying has the run time of --> O(apply)
                self.AppliedLayer.append(LayerEffect) #Appending in a circular queue is constant --> O(1)
        return start #Returning is always constant --> O(1)
        

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Args:
        - self
        - layer = Layer which is going to be erased

        Raises:
        - Does not raise any errors

        Returns:
        - If stack is not empty, the LayerStore was changed and will return True
        - If the stack is empty, the LayerStore was not changed and will return False

        Complexity:
        - Regardless of if the stack is empty or not, every operation is of constant run tme
          therefore, best case will be equal to the worst case, being, best case = worst case = O(1)
        """
        if not self.AppliedLayer.is_empty(): #Integer comparison is always constant --> O(1)
            self.AppliedLayer.serve() #Serving in a circular queue is always constant --> O(1)
            self.size -= 1 # size will only increase once, therefore is constant --> O(1)
            return True #Returning is always constant --> O(1)
        else: #Integer comparison is always constant --> O(1)
            return False #Returning is always cosntant --> O(1)

            

    
    def special(self):
        """
        Special mode. Different for each store implementation.

        Args:
        - self

        Raises:
        - If queue is empty, raise error: Queue is empty

        Returns:
        - Does not return anything

        Complexity:
        - If the original queue is empty, then the time complexity cannot be analysed as raising does not have a complexity.
        - If the Queue is not empty, then the best case is equal to the worst case which will be O(self.size + k) + O(self.size + k),
          therefore, best = worst = O(self.size + k) + O(self.size + k). 
        """
        NewStack = ArrayStack(len(self.AppliedLayer) * 1000) #Constant --> O(1)
        NewQueue = CircularQueue(len(self.AppliedLayer) * 1000) #Constant --> O(1)

        if self.AppliedLayer.is_empty(): #Assingment comparison is always constant --> O(1)
            raise "Queue is empty" #No complexity analysis of raisng 

        
        if not self.AppliedLayer.is_empty(): #Integer comparison is always constant --> O(1)
            for _ in range(self.size): #Will run for self.size times
                ServedValue = self.AppliedLayer.serve() #Serving for a circular queue is always constant --> O(1)
                NewStack.push(ServedValue) #Pushing in a stack is always constant --> O(1)


            for _ in range(self.size): #will run for self.size times
                item  = NewStack.pop() #Popping is always constant --> O(1)
                NewQueue.append(item) #Appending is always constant --> O(1)
            self.AppliedLayer = NewQueue #Assignment is alway constant --> O(1)  
                 

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        self.MAX_CAPACITY = 20 #Assignment is constant --> O(1)
        self.AddSorted = ArraySortedList(self.MAX_CAPACITY) #Assignment is constant --> O(1)
        self.all_layers = get_layers() #Assignment is constant --> O(1)
        

  
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Args:
        - layer = The layer that is going to be added
        - self

        Raises:
        - Does not raise any errors

        Returns:
        - If the current layer is not in the Sorted list, it will return True
        - If the current layer is in the Sorted List, it will return False

        Complexity:
        - As every operation in the function is constant, the best case is equal to the 
          worst case, therefore best = worst = O(1)
        """
        current_layer = ListItem(layer,layer.index)  #Setting list item is constant --> O(1)

        if current_layer not in self.AddSorted: #Integer comparison is always constant --> O(1)
            self.AddSorted.add(current_layer) # Sorted list add is always constant --> O(1)
            return True # Returning is always constant --> O(1)
        else: #Integer comparison is always constant --> O(1)
            return False  #Returning is always constant --> O(1)      

        
        
        

  
    def get_color(self, start: tuple, timestamp: float, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - start = tuple which represents the starting color
        - timestamp = Used by some layers for dynamic effects and it is a float
        - x = x dimnesion of the grid and it is an int
        - y = y dimension of the grid and it is an int
        - self

        Raises:
        - There are no raises

        Returns:
        - Returns the effected color tuple

        Complexity:
        - As the function is entirely dependent on looping through the layers, the best case will
          always be equal to the worst case. The loop will always run for len(self.AddSorted) times with 
          apply running each time. Therefore, the best = worst = O(self.AddSorted + apply + k), where k is 
          an integer representing the constant operations. 
        """
        returning_val = start #Assignment is always constant --> O(1)
        if not self.AddSorted.is_empty(): #Integer comparison is always constant --> O(1)
            for i in range(len(self.AddSorted)): #Runs for len(self.Addsorted) times --> O(len(self.AddSorted))
                current_layer = self.AddSorted[i] # Assigment is always constant --> O(1)
                returning_val = current_layer.value.apply(returning_val,timestamp,x,y) #Apply has it run time of --> O(apply)
        return returning_val #Returning is always constant --> O(1)        

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Args:
        - self
        - layer = the layer that is going to be erased

        Raises:
        - Does not raise any errors

        Returns:
        - If the Sorted list is empty, then it will return False
        - If it is not empty, then it will return True

        Complexity:
        - The for loop will always run for len(self.AddSorted) times. the best case is 
          if the index looking to be deleted is in the last position, in which it will only take one step.
          Therefore, the best case  = O(k) + O(k) + O(len(self.AddSorted)) = O(len(self.AddSorted) + k), where k is
          an integer representing the other constant operations. The worst case is if the index looking to be deleted
          is at the front in which it will need to traverse through the whole sorted list. Therefore, 
          the worst case = O(k) + O(len(self)) + O(len(self.AddSorted)) = O(k + len(self) + len(self.AddSorted))
         """
        if self.AddSorted.is_empty(): #Integer comparison is always constant --> O(1)
            return False #Return statements is always constant --> O(1)
        for i in range(len(self.AddSorted)): #Will run for len(self.AddSorted) times
            if (layer.index) == self.AddSorted[i].key: #Integer comparison is always constant --> O(1)
                self.AddSorted.delete_at_index(i) #If index is in last position then O(1), if index is at the front then O(len(self))
                return True #Return statements are always constant --> O(1)
            
        return False    #Return statements are always constant --> O(1)

    
    def special(self):
        """
        Special mode. Different for each store implementation.

        Args:
        - self

        Raises:
        - Does not raise any errors

        Returns:
        - Does not return any statements 

        Complexity:
        - The loop will always run for len(self.AddSorted) times. Best case is if the item which is being
          added into the temporary sorted list is at the end of the list and the deleted index is in the last position,
          in which the best case = O(len(self.AddSorted) + O(log(len(self))) + O(k) where k is an integer which
          represents the constant operations performed including the delete_at_index() if the index is in the last position.
          The worst case is if the item being added is at the start of the list and the index being deleted is also at the
          start of the list, in which worst case = O(len(self)) + O(len(self.AddSorted)) + O(k) where k is an integer which
          represents the constant operations performed.
        """
        
        tmp_sorted_list = ArraySortedList(self.MAX_CAPACITY) #Assignment is always constant --> O(1)
        n = len(self.AddSorted) #Assignment is always constant --> O(1)
        

        
        

        for i in range(n): #Will run for len(self.AddSorted) times
            if not self.AddSorted[i] == None: #Comparison is always constant --> O(1)
                CurrentLayer = self.AddSorted[i] #Comparison is always constant --> O(1)
                AddedIndex = ListItem(i,CurrentLayer.value.name) #List item is always constant --> O(1)
                tmp_sorted_list.add(AddedIndex) #Depending on position of item, can vary in time complexities
               

        #Print the median of a list of names
        if len(self.AddSorted)!=0: #Comparison is always constant --> O(1)
            if len(self.AddSorted) % 2 == 0: #Comparison is always constant --> O(1)
                self.AddSorted.delete_at_index(tmp_sorted_list[(n//2)-1].value) #If index is in last position then O(1), if index is at the front then O(len(self))
            else: #Comparison is always constant --> O(1)
                self.AddSorted.delete_at_index(tmp_sorted_list[n//2].value) #If index is in last position then O(1), if index is at the front then O(len(self))







