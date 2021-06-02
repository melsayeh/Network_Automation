def multitable(number):
    i = 0
    if not number.isdigit():
        print("This is not a number, try again ...")
        return
    else:
        while i < 12:
            i = i + 1
            y = int(number) * i
            print(number, " x ", i, " = ", y)


x = input("Enter a number:")
multitable(x)
