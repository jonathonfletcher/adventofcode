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

type Grid struct {
	width  int
	height int
	maxX   int
	maxY   int
	values [][]int
}

func (grid *Grid) Init(width int, height int) {
	grid.width = width
	grid.height = height
	grid.values = make([][]int, grid.height)
	for y := 0; y < grid.width; y++ {
		grid.values[y] = make([]int, grid.width)
	}
}

func (grid *Grid) Set(x int, y int, v int) {
	if x > grid.maxX {
		grid.maxX = x
	}
	if y > grid.maxY {
		grid.maxY = y
	}
	grid.values[y][x] = v
}

func (grid *Grid) SizeBasin(x int, y int) int {

	type point struct {
		x int
		y int
	}

	seenPoints := make(map[string]bool)

	if grid.values[y][x] < 9 {
		var visitPoints []point = nil
		visitPoints = append(visitPoints, point{x, y})

		seenPoints[fmt.Sprint(x, ",", y)] = true
		for len(visitPoints) > 0 {
			// log.Println(visitPoints)
			var newVisitPoints []point = nil
			for _, v := range visitPoints {
				var points = []point{
					{x: v.x - 1, y: v.y},
					{x: v.x + 1, y: v.y},
					{x: v.x, y: v.y - 1},
					{x: v.x, y: v.y + 1},
				}
				for _, p := range points {
					if p.x >= 0 && p.y >= 0 && p.x <= grid.maxX && p.y <= grid.maxY {
						if grid.values[p.y][p.x] < 9 && !seenPoints[fmt.Sprint(p.x, ",", p.y)] {
							seenPoints[fmt.Sprint(p.x, ",", p.y)] = true
							newVisitPoints = append(newVisitPoints, p)
						}
					}
				}
			}
			visitPoints = newVisitPoints
		}
	}

	return len(seenPoints)
}

func (grid *Grid) IsLow(x int, y int) bool {
	type point struct {
		x int
		y int
	}

	var points = []point{
		{x: x - 1, y: y},
		{x: x + 1, y: y},
		{x: x, y: y - 1},
		{x: x, y: y + 1},
	}

	v := grid.values[y][x]
	for _, p := range points {
		tv := 9
		if p.x >= 0 && p.y >= 0 && p.x <= grid.maxX && p.y <= grid.maxY {
			tv = grid.values[p.y][p.x]
			if tv <= v {
				return false
			}
		}
	}

	return true
}

func (grid *Grid) FindRisk(calcBasin bool) int {
	risk := 0
	basins := []int{}
	for y := 0; y <= grid.maxY; y++ {
		for x := 0; x <= grid.maxX; x++ {
			if grid.IsLow(x, y) {
				if calcBasin {
					basinSize := grid.SizeBasin(x, y)
					// log.Println("(", x, ",", y, ")", grid.values[y][x], basinSize)
					basins = append(basins, basinSize)
				} else {
					// log.Println(x, y, grid.values[y][x])
					risk += 1 + grid.values[y][x]
				}
			}
		}
	}
	if calcBasin && len(basins) > 0 {
		sort.Sort(sort.Reverse(sort.IntSlice(basins)))
		// log.Println(basins)
		risk = 1
		for i := 0; i < 3 && i < len(basins); i++ {
			risk *= basins[i]
		}
	}
	return risk
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		var grid *Grid = nil
		y := 0
		for scanner.Scan() {
			inputSVs := strings.Split(scanner.Text(), "")
			if grid == nil {
				grid = new(Grid)
				grid.Init(len(inputSVs), len(inputSVs))
			}
			for x, sv := range inputSVs {
				iv, _ := strconv.Atoi(sv)
				grid.Set(x, y, iv)
			}
			y++
		}
		inFile.Close()
		// log.Println(*grid)
		log.Println(grid.FindRisk(false))
		log.Println(grid.FindRisk(true))
	}
}
