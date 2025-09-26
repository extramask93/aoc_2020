from enum import StrEnum
from collections import deque
from functools import reduce

class Context:
    def __init__(self):
        self.ip = 0
        self.accumulator = 0

class Instruction:
    def __init__(self):
        self.visited = False
        self.reachable_end = False
        self.nxt = None
        self.prevs = []
    def execute(self, context: Context):
        pass
class Accumulate(Instruction):
    def __init__(self, argument: int):
        super().__init__()
        self.argument = argument
    def execute(self, context: Context):
        context.accumulator += self.argument
        context.ip += 1
        return context
    def __str__(self):
        return f"acc {self.argument}"
class Nop(Instruction):
    def __init__(self, argument: int):
        super().__init__()
        self.argument = argument
    def execute(self, context):
        context.ip +=1
        return context
    def __str__(self):
        return f"Nop {self.argument}"
class Jump(Instruction):
    def __init__(self, argument: int):
        super().__init__()
        self.argument = argument
    def execute(self, context):
        context.ip += self.argument
        return context
    def __str__(self):
        return f"Jump {self.argument}"
def from_text(line:str) -> Instruction:
    operation, argument = line.split()
    argument = int(argument)
    operation = operation.strip()
    if operation == "acc":
        return Accumulate(argument)
    if operation == "jmp":
        return Jump(argument)
    if operation == "nop":
        return Nop(argument)
    else:
        print(f"unknown: {operation}")

if __name__ == "__main__":
    ops = []
    context = Context()
    with open("inputs/day8.txt") as file:
        for line in file:
            ops.append(from_text(line))
    #Create Directed Graph
    for cnt, op in enumerate(ops):
        if isinstance(op,(Accumulate, Nop)):
            if cnt+1 < len(ops):
                op.nxt = ops[cnt+1]
        else:
            if cnt+op.argument < len(ops):
                op.nxt = ops[cnt+op.argument]
        if op.nxt:
            op.nxt.prevs.append(op)
    #find a loop
    current_op = ops[0]
    while not current_op.visited:
        current_op.execute(context)
        current_op.visited = True
        current_op = current_op.nxt
    print(context.accumulator)
    #### part 2
    #Find all nodes reachable from last node
    for op in ops:
        op.visited=False
    queue = deque()
    queue.append(ops[-1])
    while queue:
        node = queue.popleft()
        if not node.visited:
            queue.extend(node.prevs)
            node.reachable_end = True
            node.visited = True
    
    context = Context()
    flipped = False
    while context.ip < len(ops):
        current_op = ops[context.ip]
        if not flipped and isinstance(current_op, Jump):
            if context.ip+1 < len(ops) and ops[context.ip+1].reachable_end:
                current_op = Nop(current_op.argument)
                flipped = True
        elif not flipped and isinstance(current_op, Nop):
            if (context.ip+current_op.argument < len(ops)) and (ops[context.ip+current_op.argument].reachable_end):
                current_op = Jump(current_op.argument)
                flipped = True
        current_op.execute(context)
    print(context.accumulator)

    
        


        
    
    
    
    