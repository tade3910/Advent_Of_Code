#!/usr/bin/python3
from collections import deque

def blink(max_level: int, input: str) -> int:
    cache = {}  # Cache for computed results
    queue = [int(s) for s in input.split()]  # Queue of (stone, level)
    # result_count = 0
    for _ in range(max_level):
        nextQueu = []
        for stone in queue:
            if stone in cache:
                transformed = cache[stone]
            else:
                transformed = transform(stone)
                cache[stone] = transformed
            for new_stone in transformed:
                nextQueu.append(new_stone)
        queue = nextQueu
    return len(queue)

def optimized_blinks(max_level: int, input: str) -> int:
    cache = {} 
    queue = {}  
    for s in input.split():
        queue[s] = queue.get(s, 0) + 1
    for _ in range(max_level):
        updated_queue = {}        
        for stone, count in queue.items():
            stone = int(stone)
            if stone in cache:
                transformed = cache[stone]
            else:
                transformed = transform(stone)
                cache[stone] = transformed
            
            for next_stone in transformed:
                updated_queue[next_stone] = updated_queue.get(next_stone, 0) + count
        queue = updated_queue
    return sum(queue.values())

def transform(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        mid = len(s) // 2
        left = int(s[:mid])
        right = int(s[mid:])
        return [left, right]
    else:
        val = int(stone) * 2024
        return [val]

print(blink(25, "2 77706 5847 9258441 0 741 883933 12"))
print(optimized_blinks(75, "2 77706 5847 9258441 0 741 883933 12"))
