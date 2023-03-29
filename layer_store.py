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

    MAX_CAPACITY = 1
    
    
    def __init__(self) -> None:
        self.LayerApplied = ArrayStack(self.MAX_CAPACITY)
        self.flag = False
        
    
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        
        if len(self.LayerApplied) < self.MAX_CAPACITY:
            self.LayerApplied.push(layer)
            return True
        else:
            self.LayerApplied.clear()
            self.LayerApplied.push(layer)
        return False
             

    
    def get_color(self,start,timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if not self.flag:
            if not self.LayerApplied.is_empty():
                effect = self.LayerApplied.peek()
                start = effect.apply(start,timestamp,x,y)
                return start
            if self.LayerApplied.is_empty():
                return start
        else:
            if self.LayerApplied.is_empty():
                return start 
           
            if not self.LayerApplied.is_empty():
                effect = self.LayerApplied.peek()
                start = effect.apply(start,timestamp,x,y)
                start = invert.apply(start,timestamp,x,y)
        return start
          
        
       
    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.LayerApplied.is_empty():
            return False
        else:
            self.LayerApplied.pop()
            return True    

      

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        self.flag = not self.flag
        
            
        
        

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    MAX_CAPACITY = 100

    def __init__(self) -> None:
        self.AppliedLayer = CircularQueue(self.MAX_CAPACITY)
        
        
    
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if not self.AppliedLayer.is_full(): #Checking if it is full
            self.AppliedLayer.append(layer)
            return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.AppliedLayer.is_empty():
            return start 
           
        for i in range(len(self.AppliedLayer)):
            if not self.AppliedLayer.is_empty():
                LayerEffect = self.AppliedLayer.serve()
                start = LayerEffect.apply(start,timestamp,x,y)
                self.AppliedLayer.append(LayerEffect)
        return start
        

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if not self.AppliedLayer.is_empty():
            self.AppliedLayer.serve()
            return True
        else:
            return False    

            

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        MyStack = ArrayStack(len(self.AppliedLayer))

        

        
        if not self.AppliedLayer.is_empty():
            for _ in range(len(self.AppliedLayer)):
                ServedValue = self.AppliedLayer.serve()
                MyStack.push(ServedValue)

            while not MyStack.is_empty():
                item  = MyStack.pop()
                self.AppliedLayer.append(item)
                 

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
        self.MAX_CAPACITY = 20
        self.AddSorted = ArraySortedList(self.MAX_CAPACITY)
        self.all_layers = get_layers()
        

  
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        #if self.AddSorted.is_full():
            #return False

        current_layer = ListItem(layer,layer.index)

        if current_layer not in self.AddSorted:
            self.AddSorted.add(current_layer)
            return True
        else:
            return False        

        
        
        

  
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        returning_val = start
        if not self.AddSorted.is_empty():
            for i in range(len(self.AddSorted)):
                current_layer = self.AddSorted[i]
                returning_val = current_layer.value.apply(returning_val,timestamp,x,y)
        return returning_val        
                  





    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.AddSorted.is_empty():
            return False
        for i in range(len(self.AddSorted)):
            if (layer.index) == self.AddSorted[i].key:
                self.AddSorted.delete_at_index(i)
                return True
            
        return False    

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        
        tmp_sorted_list = ArraySortedList(self.MAX_CAPACITY)
        n = len(self.AddSorted)
        

        
        

        for i in range(n):
            if not self.AddSorted[i] == None:
                CurrentLayer = self.AddSorted[i]
                AddedIndex = ListItem(i,CurrentLayer.value.name)
                tmp_sorted_list.add(AddedIndex)
               

        #Print the median of a list of names
        if len(self.AddSorted)!=0:
            if len(self.AddSorted) % 2 == 0:
                self.AddSorted.delete_at_index(tmp_sorted_list[(n//2)-1].value)
            else:
                self.AddSorted.delete_at_index(tmp_sorted_list[n//2].value) 







