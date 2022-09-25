number = int(input("Type a number: "))

numberDict = {}
for i in range(1, number+1):
    numberDict[i] = i*i

print(numberDict)