package main

import (
	"bufio"
	"fmt"
	"os"
)

const Start = 'S'
const Beam = '|'
const Splitter = '^'

func getManifold(filename string) [][]rune {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	manifold := [][]rune{}
	for scanner.Scan() {
		line := []rune(scanner.Text())
		manifold = append(manifold, line)
	}
	return manifold
}

func part1(filename string) {
	manifold := getManifold(filename)
	for index, r := range manifold[0] {
		if r == Start {
			manifold[1][index] = Beam
			break
		}
	}
	sum := 0
	for i := 1; i < len(manifold)-1; i++ {
		row := manifold[i]
		for j, r := range row {
			if r == Beam {
				switch manifold[i+1][j] {
				case Splitter:
					manifold[i+1][j-1] = Beam
					manifold[i+1][j+1] = Beam
					sum++
				default:
					manifold[i+1][j] = Beam
				}
			}
		}
	}

	fmt.Printf("Sum is %d\n", sum)
}

type Entry struct {
	Row int
	Col int
}

type Stack struct {
	entries []*Entry
}

func (s *Stack) Push(row, col int) {
	s.entries = append(s.entries, &Entry{
		Row: row,
		Col: col,
	})
}

func (s *Stack) Empty() bool {
	return len(s.entries) <= 0
}

func (s *Stack) Pop() *Entry {
	if s.Empty() {
		return nil
	}
	val := s.entries[len(s.entries)-1]
	s.entries = s.entries[:len(s.entries)-1]
	return val
}

// O(I don't even want to think of it)
func part2(filename string) {
	manifold := getManifold(filename)
	pathStack := Stack{}
	for index, r := range manifold[0] {
		if r == 'S' {
			pathStack.Push(1, index)
			break
		}
	}
	sum := 0
	endRow := len(manifold) - 1
	for !pathStack.Empty() {
		cur := pathStack.Pop()
		// row, col := cur.Row, cur.Col
		//keep going through rows until we see split
		row := cur.Row + 1
		for row < endRow {
			r := manifold[row][cur.Col]
			if r == Splitter {
				pathStack.Push(row, cur.Col-1)
				pathStack.Push(row, cur.Col+1)
				break
			}
			row++
		}
		if row >= endRow {
			sum++
		}

	}
	fmt.Printf("Sum is %d\n", sum)
}

// Instead of actually trying all possibilities
// just keep track of how many possible ways
// beam can get to position
// going row by row we add other beams that at that point
// O(n)
func bigBrain2(filename string) {
	manifold := getManifold(filename)
	posibilites := make(map[int]map[int]int)
	for i := range len(manifold) {
		posibilites[i] = map[int]int{}
	}
	for index, r := range manifold[0] {
		if r == Start {
			posibilites[1][index] = 1
			break
		}
	}

	for i := 1; i < len(manifold)-1; i++ {
		for col, count := range posibilites[i] {
			r := manifold[i+1][col]
			switch r {
			case Splitter:
				curLeft, leftOk := posibilites[i+1][col-1]
				leftCount := count
				if leftOk {
					leftCount = count + curLeft
				}
				posibilites[i+1][col-1] = leftCount
				curRight, rightOk := posibilites[i+1][col+1]
				rightCount := count
				if rightOk {
					rightCount = count + curRight
				}
				posibilites[i+1][col+1] = rightCount
			default:
				curDown, downOk := posibilites[i+1][col]
				downCount := count
				if downOk {
					downCount = count + curDown
				}
				posibilites[i+1][col] = downCount
			}
		}
	}
	sum := 0
	for _, count := range posibilites[len(manifold)-1] {
		sum += count
	}
	fmt.Printf("Sum is %d\n", sum)
}

func main() {
	// part1("sample.txt")
	// part1("input.txt")
	// part2("sample.txt")
	bigBrain2("input.txt")
	// part2("input.txt")
}
