from referential_array import ArrayR

GridArray = ArrayR(9)
for i in range(3):
    ListArray = ArrayR(3)
    for j in range(3):
        ListArray.__setitem__(j,"")
GridArray.__setitem__(i,ListArray)

dog=GridArray[0][0]
GridArray[1] = 6

x = range(0,9)

first = GridArray[1]
print(dog)
