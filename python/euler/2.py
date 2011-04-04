


stack = [1, 2]

while stack[-1] < 4000000:
    stack.append(stack[-1] + stack[-2]) 

even = [x for x in stack if x % 2 == 0]

print sum(even)
