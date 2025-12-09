package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Point struct {
	X, Y int
}

type Rectangle struct {
	P1   Point
	P2   Point
	Area int
}

func Init(P1, P2 Point) Rectangle {
	return Rectangle{
		P1:   P1,
		P2:   P2,
		Area: Area(P1, P2),
	}
}

func Area(p1, p2 Point) int {
	height := max(p1.Y, p2.Y) - min(p1.Y, p2.Y) + 1
	width := max(p1.X, p2.X) - min(p1.X, p2.X) + 1
	return height * width
}

func SortPointByArea(points []Point) []Rectangle {
	response := []Rectangle{}
	for i := range points {
		for j := i + 1; j < len(points); j++ { // Only do each pair once
			response = append(response, Init(points[i], points[j]))
		}
	}

	sort.Slice(response, func(i, j int) bool {
		return response[i].Area > response[j].Area
	})

	return response
}

type Tile int

const (
	Empty Tile = iota
	Red
	Green
)

//	func FloodFill(grid [][]Tile, row, col int) {
//		if row < 0 || row >= len(grid) || col < 0 || col >= len(grid[0]) {
//			return
//		}
//		if grid[row][col] != Empty {
//			return
//		}
//		grid[row][col] = Green
//		FloodFill(grid, row-1, col)
//		FloodFill(grid, row+1, col)
//		FloodFill(grid, row, col-1)
//		FloodFill(grid, row, col+1)
//	}
func FloodFill(grid [][]Tile, r, c int) {
	rows := len(grid)
	cols := len(grid[0])

	// If starting point is not empty, no fill
	if grid[r][c] != Empty {
		return
	}

	stack := []Point{{c, r}} // (X,Y) but X=col, Y=row
	grid[r][c] = Green

	for len(stack) > 0 {
		// pop
		p := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		dirs := [][2]int{
			{0, 1}, {0, -1}, {1, 0}, {-1, 0},
		}

		for _, d := range dirs {
			nr, nc := p.Y+d[1], p.X+d[0]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols {
				if grid[nr][nc] == Empty {
					grid[nr][nc] = Green
					stack = append(stack, Point{nc, nr})
				}
			}
		}
	}
}

func PrintGrid(grid [][]Tile) {
	for _, row := range grid {
		fmt.Printf("%d\n", row)
	}
	fmt.Println()
}

func FillGrid(points []Point, maxRow, minRow, maxCol, minCol, floodRow, floodCol int) {
	rows := maxRow - minRow + 1
	cols := maxCol - minCol + 1
	grid := make([][]Tile, rows)
	for i := range rows {
		grid[i] = make([]Tile, cols)
	}

	for _, point := range points {
		grid[point.Y-minRow][point.X-minCol] = Red
	}
	// PrintGrid(grid)

	//Outline Grid
	for i, p1 := range points {
		for j := i + 1; j < len(points); j++ {
			p2 := points[j]
			if p1.X == p2.X {
				//On same col
				col := p1.X
				for row := min(p1.Y, p2.Y) + 1; row < max(p1.Y, p2.Y); row++ {
					grid[row][col] = Green
				}
			} else if p1.Y == p2.Y {
				//on same row
				row := p1.Y
				for col := min(p1.X, p2.X) + 1; col < max(p1.X, p2.X); col++ {
					grid[row][col] = Green
				}
			}
		}
		// p2 := points[(i+1)%n] // wrap to first tile
		// if p1.X == p2.X {     // same column
		// 	startRow := min(p1.Y, p2.Y)
		// 	endRow := max(p1.Y, p2.Y)
		// 	for r := startRow + 1; r < endRow; r++ {
		// 		curRow := r - minRow
		// 		curCol := p1.X - minCol
		// 		// fmt.Printf("Testing %d %d \n", curRow, curCol)
		// 		grid[curRow][curCol] = Green
		// 	}
		// } else if p1.Y == p2.Y { // same row
		// 	startCol := min(p1.X, p2.X)
		// 	endCol := max(p1.X, p2.X)
		// 	for c := startCol + 1; c < endCol; c++ {

		// 		grid[p1.Y-minRow][c-minCol] = Green
		// 	}
		// } else {
		// 	// should never happen; adjacent points are always on same row or column
		// }
	}
	// PrintGrid(grid)

	FloodFill(grid, floodRow, floodCol)
	// PrintGrid(grid)

	sortedRectangles := SortPointByArea(points)
	for _, rect := range sortedRectangles {
		p1, p2 := rect.P1, rect.P2
		startRow := min(p1.Y, p2.Y)
		startCol := min(p1.X, p2.X)
		endRow := max(p1.Y, p2.Y)
		endCol := max(p1.X, p2.X)
		valid := true
		for i := startRow; i <= endRow && valid; i++ {
			for j := startCol; j <= endCol && valid; j++ {
				if grid[i-minRow][j-minCol] == Empty {
					valid = false
					break
				}
			}
			if !valid {
				break
			}
		}
		if valid {
			fmt.Printf("Max area is %d\n", rect.Area)
			break
		}
	}

}

func SortPointByValidArea(points []Point) []Rectangle {
	type minmax struct {
		min, max int
	}
	minRow, maxRow := points[0].Y, points[0].Y
	rowMinMax := make(map[int]*minmax)
	for _, point := range points {
		col, row := point.X, point.Y
		val, inMap := rowMinMax[row]
		if inMap {
			rowMinMax[row].max = max(val.max, col)
			rowMinMax[row].min = min(val.min, col)
		} else {
			rowMinMax[row] = &minmax{col, col}
		}
		minRow, maxRow = min(minRow, row), max(maxRow, row)
	}
	sliceRowMinMax := make([]*minmax, maxRow-minRow+1)
	sliceRowMinMax[0] = rowMinMax[minRow]
	index := 1
	for i := minRow + 1; i <= maxRow; i++ {
		prevMinMax := sliceRowMinMax[index-1]
		prevEntry, prevOk := rowMinMax[i-1]
		curMinMax, ok := rowMinMax[i]
		editing := &minmax{}
		if ok {
			//Red on red
			//Stretch out to allow above column to be paried
			editing.min = min(prevMinMax.min, curMinMax.min)
			editing.max = max(prevMinMax.max, curMinMax.max)
		} else if !prevOk {
			//Propogating down above
			//Take above values
			editing.min = prevMinMax.min
			editing.max = prevMinMax.max
		} else {
			//Red above
			//Current on green so stretch to top red
			if prevEntry.min > prevMinMax.min {
				//preveEntry was grown left because of parent
				editing.min = prevMinMax.min
				editing.max = prevEntry.min
			} else if prevEntry.max < prevMinMax.max {
				//was grown right for parent
				editing.max = prevMinMax.max
				editing.min = prevEntry.max
			} else {
				editing.min = prevMinMax.min
				editing.max = prevMinMax.max
			}
		}
		sliceRowMinMax[index] = editing
		index++
	}
	response := []Rectangle{}
	for i := range points {
		for j := i + 1; j < len(points); j++ { // Only do each pair once
			iPoint := points[i]
			jPoint := points[j]
			iCol, iRow := iPoint.X, iPoint.Y
			jCol, jRow := jPoint.X, jPoint.Y
			iVal := rowMinMax[iRow]
			jVal := rowMinMax[jRow]
			if iVal.max < jCol || iVal.min > jCol || jVal.max < iCol || jVal.min > iCol {
				continue
			}
			response = append(response, Init(iPoint, jPoint))
		}
	}
	sort.Slice(response, func(i, j int) bool {
		return response[i].Area > response[j].Area
	})

	return response
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

func part2(filename string, floodRow, floodCol int) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	points := []Point{}
	maxRow, minRow, maxCol, minCol := 0, -1, 0, -1

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ",")
		x, y := getInt(line[0]), getInt(line[1])
		maxRow = max(maxRow, y)
		if minRow == -1 {
			minRow = y
		} else {
			minRow = min(minRow, y)
		}
		maxCol = max(maxCol, x)
		if minCol == -1 {
			minCol = x
		} else {
			minCol = min(minCol, x)
		}
		points = append(points, Point{
			x, y,
		})
	}
	FillGrid(points, maxRow, minRow, maxCol, minCol, floodRow, floodCol)
}

func main() {
	// part2("sample.txt",2,7)
	part2("input.txt", 48729, 96346)

	// part1("sample.txt")
	// part1("input.txt")
	// part2("input.txt")

}

func part1(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	points := []Point{}
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ",")
		points = append(points, Point{
			getInt(line[0]),
			getInt(line[1]),
		})
	}
	sortedSlice := SortPointByArea(points)
	fmt.Printf("Largest area is %d\n", sortedSlice[0].Area)
}
