import itertools
times=0
combinations = list(itertools.product(["G", "W"], repeat=9))
for combination in combinations:
    board = [combination[i:i+3] for i in range(0, len(combination), 3)]
    squareId = ''.join(str(i) for i in board)
    squareId = "".join([i if i in ["G", "W"] else "" for i in squareId])
    if squareId[4] == "G" and "W" in squareId:
        times +=1
        print(f"---{times}---------{board}    {squareId}")
        print(f"elif squareId == {squareId}")
        for row in board:
            print("".join(row))
        print()
        print()
