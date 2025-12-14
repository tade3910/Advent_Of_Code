package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
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

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// Regex to detect "4x4:" or "12x5:" etc
	sizeLine := regexp.MustCompile(`^\d+x\d+:`)

	currentID := ""
	hashCount := 0
	readingBlock := false
	counts := []int{}
	var validRegions int

	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)

		if line == "" {
			// Blank line ends a block
			if readingBlock {
				counts = append(counts, hashCount)
				fmt.Printf("Block %s has %d # characters\n", currentID, hashCount)
				readingBlock = false
				hashCount = 0
			}
			continue
		}

		// If it's a block header like "3:"
		if strings.HasSuffix(line, ":") && !sizeLine.MatchString(line) {
			// e.g. "5:" → start a new block
			currentID = strings.TrimSuffix(line, ":")
			readingBlock = true
			hashCount = 0
			continue
		}

		// If it's a size line like "4x4:" or "12x5:"
		if sizeLine.MatchString(line) {
			// Finish the current block BEFORE the size line
			if readingBlock {
				counts = append(counts, hashCount)
				fmt.Printf("Block %s has %d # characters\n", currentID, hashCount)
				readingBlock = false
				hashCount = 0
			}
			split := strings.Split(line, ":")
			availableArea := strings.Split(strings.TrimSpace(split[0]), "x")
			givenArea := getInt(availableArea[0]) * getInt(availableArea[1])
			neededCounts := strings.Split(strings.TrimSpace(split[1]), " ")
			var shapesSpace int
			for i, count := range neededCounts {
				cur := counts[i] * getInt(count)
				shapesSpace += cur
			}
			if shapesSpace <= givenArea {
				validRegions++
			}
			continue
		}

		// Otherwise it's a row like "###" or "##."
		if readingBlock {
			hashCount += strings.Count(line, "#")
		}
	}

	// Flush last block if file doesn’t end with blank line
	if readingBlock {
		fmt.Printf("Block %s has %d # characters\n", currentID, hashCount)
	}
	fmt.Printf("Counts were %d\n", counts)
	fmt.Printf("Valid regions were %d\n", validRegions)

}
