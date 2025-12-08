package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Point struct {
	X, Y, Z int
}

type PointTuple struct {
	P1 *Point
	P2 *Point
}

func EuclideanDistance(p1, p2 Point) float64 {
	dx := p2.X - p1.X
	dy := p2.Y - p1.Y
	dz := p2.Z - p1.Z
	return math.Sqrt(float64(dx*dx + dy*dy + dz*dz))
}

func SortPointByDistance(points []Point) []*PointTuple {
	response := []*PointTuple{}
	for i := range points {
		for j := i + 1; j < len(points); j++ { // Only do each pair once
			response = append(response, &PointTuple{
				P1: &points[i],
				P2: &points[j],
			})
		}
	}

	sort.Slice(response, func(i, j int) bool {
		iDistance := EuclideanDistance(*response[i].P1, *response[i].P2)
		jDistance := EuclideanDistance(*response[j].P1, *response[j].P2)
		return iDistance < jDistance
	})
	return response
}

type Tracker struct {
	parent []int
	size   []int
}

func NewTracker(numElements int) *Tracker {
	parent := make([]int, numElements)
	size := make([]int, numElements)
	for i := range numElements {
		parent[i] = i //All start as each is parent of themselves
		size[i] = 1
	}
	return &Tracker{parent, size}
}

func (t *Tracker) FindParent(x int) int {
	for x != t.parent[x] {
		x = t.parent[x]
	}
	return x
}

// Return true if all connected
func (t *Tracker) Union(x, y int) bool {
	xRoot := t.FindParent(x)
	yRoot := t.FindParent(y)
	if xRoot == yRoot {
		return false
	}
	// Union by size
	if t.size[xRoot] < t.size[yRoot] {
		xRoot, yRoot = yRoot, xRoot
	}

	t.parent[yRoot] = xRoot
	t.size[xRoot] += t.size[yRoot]
	t.size[yRoot] = 0
	//All connected when size == number of elements
	return t.size[xRoot] == len(t.size)
}

func (t *Tracker) ComponentSizes() []int {
	m := make(map[int]int)
	for i := range t.parent {
		root := t.FindParent(i)
		m[root]++
	}
	res := []int{}
	for _, sz := range m {
		res = append(res, sz)
	}
	return res
}

func indexOf(points []Point, point Point) int {
	for i, cur := range points {
		if cur == point {
			return i
		}
	}
	panic("oogie boogie")
}

func MakeXConnections(points []Point, numConnections int) {
	sortedPairs := SortPointByDistance(points)
	tracker := NewTracker(len(points))
	connections := 0
	for _, pair := range sortedPairs {
		i := indexOf(points, *pair.P1)
		j := indexOf(points, *pair.P2)
		connections++
		tracker.Union(i, j)
		if connections >= numConnections {
			break
		}
	}
	sizes := tracker.ComponentSizes()
	sort.Sort(sort.Reverse(sort.IntSlice(sizes)))
	product := 1
	for i := 0; i < 3 && i < len(sizes); i++ {
		product *= sizes[i]
	}
	fmt.Println(product)
}

func ConnectAll(points []Point) {
	sortedPairs := SortPointByDistance(points)
	tracker := NewTracker(len(points))
	for _, pair := range sortedPairs {
		i := indexOf(points, *pair.P1)
		j := indexOf(points, *pair.P2)
		if tracker.Union(i, j) {
			product := pair.P1.X * pair.P2.X
			fmt.Printf("Product is %d\n", product)
		}

	}
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
func part1(filename string, numConnections int) {
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
			getInt(line[2]),
		})
	}
	MakeXConnections(points, numConnections)
}

func part2(filename string) {
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
			getInt(line[2]),
		})
	}
	ConnectAll(points)
}

func main() {
	part1("sample.txt", 10)
	part1("sample.txt", 1000)
	part1("input.txt", 1000)
	part2("sample.txt")
	part2("input.txt")
}
