
from collections import defaultdict



if __name__ == "__main__":
    with open("inputs/day15.txt") as f:
        input = f.readline().split(",")
    input = [int(x) for x in input]

    spoken = defaultdict(list)
    previous_number = -1
    turn = -1
    for turn, said in enumerate(input,1):
        spoken[said].append(turn)
        previous_number = said
        print(f"{turn=}, {said}")
    while turn <2020:
        turn +=1
        if len(spoken[previous_number]) >=2:
            current_number = spoken[previous_number][-1] - spoken[previous_number][-2]
        else:
            current_number = 0
        spoken[current_number].append(turn)
        previous_number = current_number
    print(f"{turn=}, {current_number}")
