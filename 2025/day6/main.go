package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

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

func solve_problem(problems [][]string) int {
	total := 0
	cols := len(problems[0])
	for col := range cols {
		val := 0
		operation := problems[len(problems)-1][col]
		if operation == "*" {
			val = 1
		}
		for row := range len(problems) - 1 {
			cur := getInt(problems[row][col])
			switch operation {
			case "*":
				val *= cur
			case "+":
				val += cur
			default:
				log.Fatalf("Weird operation: %s", operation)
			}
		}
		total += val
	}
	return total
}

func removeSpaces(line string) []string {
	parsedString := []string{}
	cur_val := []rune{}
	for _, r := range line {
		if r == ' ' {
			if len(cur_val) != 0 {
				parsedString = append(parsedString, string(cur_val))
				cur_val = []rune{}
			}
		} else {
			cur_val = append(cur_val, r)
		}
	}
	if len(cur_val) != 0 {
		//Didn't end with blank
		parsedString = append(parsedString, string(cur_val))

	}
	return parsedString
}

func part1(file_name string) {
	file, err := os.Open(file_name)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	problems := [][]string{}
	for scanner.Scan() {
		line := removeSpaces(scanner.Text())
		problems = append(problems, line)
	}
	fmt.Printf("Solution is %d\n", solve_problem(problems))
}

type entry struct {
	val   rune
	index int
}

func getSolution(bucket [][]rune, operation rune) int {
	val := 0
	if operation == '*' {
		val = 1
	}
	for _, entry := range bucket {
		cur := strings.TrimSpace(string(entry))
		if cur == "" {
			continue
		}
		switch operation {
		case '*':
			val *= getInt(cur)
		case '+':
			val += getInt(cur)
		default:
			log.Fatalf("Weird operation: %c", operation)
		}
	}
	return val
}

func removeSpaces2(line string) [][]entry {
	parsedString := [][]entry{}
	cur_val := []entry{}
	for i, r := range line {
		if r == ' ' {
			if len(cur_val) != 0 {
				parsedString = append(parsedString, cur_val)
				cur_val = []entry{}
			}
		} else {
			cur_val = append(cur_val, entry{
				val:   r,
				index: i,
			})
		}
	}
	if len(cur_val) != 0 {
		//Didn't end with blank
		parsedString = append(parsedString, cur_val)

	}
	return parsedString
}

// Sigh oh sigh
func part2(file_name string) {
	file, err := os.Open(file_name)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	problems := [][][]entry{}
	for scanner.Scan() {
		line := removeSpaces2(scanner.Text())
		problems = append(problems, line)
	}
	cols := len(problems[0])
	sum := 0
	for col := cols - 1; col >= 0; col-- {
		operation := problems[len(problems)-1][col][0]
		bucket := make([][]rune, len(problems)-1)
		for row := 0; row < len(problems)-1; row++ {
			cur := problems[row][col]
			for _, e := range cur {
				index, r := e.index-operation.index, e.val
				bucket[index] = append(bucket[index], r)
			}
		}
		solution := getSolution(bucket, operation.val)
		sum += solution
	}
	fmt.Printf("Solution is %d\n", sum)
}

// Buckets get value of each column
// Go row by row add val to bucket
// Do math when you get to next operation
// This took me way longer than I want to admit
func bigBrain2(file_name string) {
	file, err := os.Open(file_name)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	problems := []string{}
	for scanner.Scan() {
		problems = append(problems, scanner.Text())
	}
	sum := 0
	col := 0
	cols := len(problems[0])
	rows := len(problems) - 1
	bucket := [][]rune{}
	operation := rune(problems[rows][col])
	initialCol := 0
	for col < cols {
		for row := range rows {
			//Make first row slice
			val := rune(problems[row][col])
			index := col - initialCol
			for i := len(bucket) - 1; i < index; i++ {
				bucket = append(bucket, []rune{})
			}
			bucket[index] = append(bucket[index], val)
		}
		col++
		if col >= cols {
			solution := getSolution(bucket, operation)
			sum += solution
		} else if problems[rows][col] == '+' || problems[rows][col] == '*' {
			//New col
			solution := getSolution(bucket, operation)
			sum += solution
			bucket = [][]rune{}
			operation = rune(problems[rows][col])
			initialCol = col
		}

	}
	fmt.Printf("Solution is %d\n", sum)

}

func main() {
	// part1("sample.txt")
	// part1("input.txt")
	// part2("sample.txt")
	// part2("input.txt")
	// bigBrain2("sample.txt")
	// bigBrain2("input.txt")
	path := strings.Split("////as///", "/")

	fmt.Printf("%s\n", path)
}
