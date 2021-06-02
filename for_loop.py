# def exp(x, y):
#     result = 1
#     for base in range(y):
#         result *= x
#     print(x, "Raised to power of", y, "is: ", result)
#
#
# x = int(input("Enter base number: "))
# y = int(input("Enter power number: "))
# exp(x, y)
from turtle import goto

number = []

while True:
    number = input("Enter a 3-digit number: ")
    if len(number) > 3:
        print("Nope! Please enter just 3-digit number, not more!")
    else:
        print("Number ", number, "has: ")
        print(number[0], "hundreds,")
        print(number[1], "tens, and")
        print(number[2], "ones.")
        break