package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const you = "you"
const end = "out"

func dfs(devices map[string][]string, paths map[string]int, val string) int {
	count, ok := paths[val]
	if ok {
		fmt.Printf("Val was %s\n", val)
		return count
	}
	var cur int
	for _, output := range devices[val] {
		if output == you {
			continue
		}
		childVal, childOk := paths[output]
		if childOk {
			cur += childVal
		} else {
			cur += dfs(devices, paths, output)
		}
	}
	paths[val] = cur
	return cur
}

func Recursive_to_end(devices map[string][]string) int {
	paths := make(map[string]int, len(devices))
	paths[end] = 1
	return dfs(devices, paths, you)
}

func dfs2(devices map[string][]string, paths map[string][][]string, val string, start string, end string) [][]string {
	if val == end {
		return [][]string{{val}}
	}
	cur := [][]string{}
	for _, output := range devices[val] {
		if output == start {
			continue
		}
		curPath := []string{val}
		childPaths, childOk := paths[output]
		if !childOk {
			childPaths = dfs2(devices, paths, output, start, end)
		}
		for _, childPath := range childPaths {
			curPath = append(curPath, childPath...)
			cur = append(cur, curPath)
		}
	}
	paths[val] = cur
	return cur
}

// func dfs3(devices map[string][]string, paths map[string]int, val string, start string, dac, fft bool, solution *int) int {
// 	_, ok := paths[val]
// 	if ok {
// 		panic("Should never hit here")
// 	}

// 	if val == "dac" {
// 		if !fft {
// 			*solution++
// 		}
// 		dac = true
// 	}
// 	if val == "fft" {
// 		if !dac {
// 			*solution++
// 		}
// 		fft = true
// 	}
// 	var cur int
// 	for _, output := range devices[val] {
// 		if output == start {
// 			continue
// 		}
// 		childResponse, childOk := paths[output]
// 		if childOk {
// 			cur += childResponse
// 		} else {
// 			childResponse := dfs3(devices, paths, output, start, dac, fft, solution)
// 			cur += childResponse
// 		}

// 	}
// 	if fft && dac {
// 		fmt.Printf("Val is %s\n", val)
// 		*solution += cur
// 	}
// 	paths[val] = cur
// 	return cur
// }

type Key struct {
	Node    string
	SeenDAC bool
	SeenFFT bool
}

func dfs3(devices map[string][]string, paths map[Key]int, node string, seenDAC, seenFFT bool) int {
	k := Key{node, seenDAC, seenFFT}
	if v, ok := paths[k]; ok {
		return v
	}

	// update flags
	if node == "dac" {
		seenDAC = true
	}
	if node == "fft" {
		seenFFT = true
	}

	if node == "out" {
		if seenDAC && seenFFT {
			return 1
		}
		return 0
	}

	total := 0
	for _, nxt := range devices[node] {
		total += dfs3(devices, paths, nxt, seenDAC, seenFFT)
	}

	paths[k] = total
	return total
}

func Recursive_to_end2(devices map[string][]string) int {
	paths := make(map[Key]int)
	return dfs3(devices, paths, "svr", false, false)
}

func Paths_to_out(devices map[string][]string) int {
	paths := make(map[string]int, len(devices))
	paths[end] = 1
	visited_paths := make(map[string]bool, len(devices))

	stack := []string{you}

	for len(stack) > 0 {
		cur := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if cur == end {
			continue
		}
		_, visited := visited_paths[cur]
		if visited {
			sum := 0
			for _, child := range devices[cur] {
				sum += paths[child]
			}
			paths[cur] = sum
			if cur == you {
				return sum
			}
			continue
		}
		visited_paths[cur] = true //Add to visited
		//Add children to be checked before we come back here
		//so on next loop we just sum it's values
		for _, child := range devices[cur] {
			if child == you {
				//Will create cycle
				continue
			}
			_, ok := paths[child]
			if !ok {
				//never explored
				stack = append(stack, child)
			}
		}

	}
	return paths[you]
}

func Part1(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	devices := make(map[string][]string)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ":")
		key := strings.TrimSpace(line[0])
		devices[key] = strings.Split(strings.TrimSpace(line[1]), " ")
	}
	fmt.Printf("Paths to out are %d\n", Recursive_to_end(devices))
}

func Part2(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	devices := make(map[string][]string)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ":")
		key := strings.TrimSpace(line[0])
		devices[key] = strings.Split(strings.TrimSpace(line[1]), " ")
	}
	fmt.Printf("Paths to out are %d\n", Recursive_to_end2(devices))
}

func main() {
	// Part1("sample.txt")
	Part1("input.txt")
	Part2("sample2.txt")
	Part2("input.txt")
}
