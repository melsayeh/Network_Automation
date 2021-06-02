number_grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [0]
]

# Use for loop to print out each individual elements
for index in range(len(number_grid)):
    for index2 in range(len(number_grid[index])):
        print(number_grid[index][index2])

##Another approach
for row in number_grid:
    print(row)
    for col in row:
        print(col)
