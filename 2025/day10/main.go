package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

func press(state []bool, button []int) {
	for _, index := range button {
		state[index] = !state[index]
	}
}

func trySequence(seq []int, buttons [][]int, expected []bool) bool {
	state := make([]bool, len(expected))

	for _, b := range seq {
		press(state, buttons[b])
	}

	for i := range state {
		if state[i] != expected[i] {
			return false
		}
	}
	return true
}

func minPresses(expected []bool, buttons [][]int) int {
	for k := 1; ; k++ {
		seqs := generateSequences(k, len(buttons))
		for _, seq := range seqs {
			if trySequence(seq, buttons, expected) {
				return k
			}
		}
	}
}

func parseExpected(token string) []bool {
	output := make([]bool, len(token))
	for i, r := range token {
		if r == '#' {
			output[i] = true
		}
	}
	return output
}
func getInt(v string) int {
	if v == "" {
		return 0
	}
	val, err := strconv.Atoi(v)
	if err != nil {
		log.Fatal(err)
	}
	return val
}

func getIntSlice(token string) []int {
	if token == "" {
		return nil
	}
	parts := strings.Split(token, ",")
	out := make([]int, len(parts))
	for i, p := range parts {
		out[i] = getInt(p)
	}
	return out
}

func part1(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var totalPresses int
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), " ")
		var buttons [][]int
		var expected []bool
		// var voltages [][]int

		for _, token := range line {
			specified := token[0]
			content := token[1 : len(token)-1]
			switch specified {
			case '[':
				expected = parseExpected(content)
			case '(':
				buttons = append(buttons, getIntSlice(content))
			default:
				// voltages = getIntSlice(content)
			}
		}
		totalPresses += minPresses(expected, buttons)
	}
	fmt.Printf("Total presses are %d\n", totalPresses)
}

func generateSequences(k int, numButtons int) [][]int {
	if k == 0 {
		return [][]int{{}}
	}

	total := int(math.Pow(float64(numButtons), float64(k)))

	seqs := make([][]int, 0, total)
	seq := make([]int, k) // current base-N counter

	for range total {
		// store a copy
		tmp := make([]int, k)
		copy(tmp, seq)
		seqs = append(seqs, tmp)
		for pos := k - 1; pos >= 0; pos-- {
			seq[pos]++
			if seq[pos] < numButtons {
				break // no carry needed
			}
			seq[pos] = 0 // wrap and carry to next digit
		}
	}

	return seqs
}

func tester() {
	output := generateSequences(3, 5)
	for _, row := range output {
		fmt.Printf("%d\n", row)
	}
}

func main() {
	// part1("sample.txt")
	// part1("input.txt")
}
