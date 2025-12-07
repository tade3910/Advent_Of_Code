#!/usr/bin/python3
from collections import deque
def optimizedBlinks(maxLevel:int,input:str):
    cache = {}
    stones = input.split(" ")
    levels = []
    done = False
    while (not done):
        updatedStonesRef, updatedLevelsRef,isDone = optimized_blink(cache, levels, stones, maxLevel)
        stones = updatedStonesRef
        levels = updatedLevelsRef
        done = isDone
    
    return len(stones)


def optimized_blink(cahce:dict, levels:list[int], stones:list[str], max_level:int):
    updated_stones = []
    updated_levels = []
    
    for i in range(len(stones)):
        stone = stones[i]
        level = levels[i] if i < len(levels) else 0  # Default level to 0 if undefined
        if level == max_level:
            updated_stones.append(stone)
            updated_levels.append(level)
        elif stone in cahce:
            next = cahce[stone]
            trace(level + 1, max_level, next, cahce, updated_levels, updated_stones)
        else:
            next = blink(stone)
            cahce[stone] = next
            updated_stones.extend(next)
            for _ in next:
                updated_levels.append(level + 1)
    
    done = all(level == max_level for level in updated_levels)
    return updated_stones, updated_levels, done


def blink(stone:str):
    updated_stones = []
    stone_length = len(stone)
    if int(stone) == 0:
        updated_stones.append("1")
    elif stone_length % 2 == 0:
        half_point = stone_length // 2
        updated_stones.append(stone[:half_point])
        second_half = stone[half_point:half_point + half_point]
        second_half = second_half.lstrip('0')
        if len(second_half) == 0: 
            second_half = '0'
        updated_stones.append(second_half)
    else:
        updated_stones.append(str(int(stone) * 2024))

    return updated_stones

def trace(cur_level:int, max_level:int, queu:list[str], cache:dict[str,list[str]], levels:list[str], updatedStones:list[str]):
    for stone in queu:
        if cur_level == max_level:
            updatedStones.append(stone)
            levels.append(cur_level)
        elif stone not in cache:
            res = blink(stone)
            cache[stone] = res
            updatedStones.extend(res)
            for _ in res:
                levels.append(cur_level + 1)
        else:
            next = cache[stone]
            trace(cur_level + 1, max_level, next, cache, levels, updatedStones)

#This shit some ass 