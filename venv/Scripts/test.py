
x= input("Enter number 1: ")

if type(x) != int:
    x = input("Dude, this is not a number! Come on, give me a real number: ")
else: pass
y= input("Enter number 2: ")
z= int(x) + int(y)
print("The output of: ", x, " - ", y, " is ", z)
