package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	FlashLimit = 9
	ResetLimit = 0
)

type Grid struct {
	width      int
	height     int
	maxX       int
	maxY       int
	values     [][]int
	hasFlashed [][]bool
}

type GridPoint struct {
	x int
	y int
}

func (grid *Grid) Init(width int, height int) {
	grid.width = width
	grid.height = height
	grid.values = make([][]int, grid.height)
	grid.hasFlashed = make([][]bool, grid.height)
	for y := 0; y < grid.width; y++ {
		grid.values[y] = make([]int, grid.width)
		grid.hasFlashed[y] = make([]bool, grid.width)
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

func (grid *Grid) FullReset() bool {
	for y := 0; y <= grid.maxY; y++ {
		for x := 0; x <= grid.maxX; x++ {
			if grid.values[y][x] != ResetLimit {
				return false
			}
		}
	}
	return true
}

func (grid *Grid) Flash() map[GridPoint]bool {
	flashes := make(map[GridPoint]bool)

	for y := 0; y <= grid.maxY; y++ {
		for x := 0; x <= grid.maxX; x++ {
			if grid.values[y][x] > FlashLimit && !grid.hasFlashed[y][x] {
				grid.hasFlashed[y][x] = true
				flashes[GridPoint{x, y}] = true
			}
		}
	}

	for p, _ := range flashes {
		neighbours := []GridPoint{
			{x: p.x - 1, y: p.y - 1},
			{x: p.x - 1, y: p.y},
			{x: p.x - 1, y: p.y + 1},
			{x: p.x, y: p.y - 1},
			{x: p.x, y: p.y + 1},
			{x: p.x + 1, y: p.y - 1},
			{x: p.x + 1, y: p.y},
			{x: p.x + 1, y: p.y + 1},
		}
		for _, n := range neighbours {
			if n.x >= 0 && n.x <= grid.maxX && n.y >= 0 && n.y <= grid.maxY {
				if grid.values[n.y][n.x] <= FlashLimit {
					grid.values[n.y][n.x] += 1
				}
			}
		}
	}

	return flashes
}

func (grid *Grid) Step() int {

	countFlashes := 0

	for y := 0; y <= grid.maxY; y++ {
		for x := 0; x <= grid.maxX; x++ {
			grid.hasFlashed[y][x] = false
			if grid.values[y][x] <= FlashLimit {
				grid.values[y][x] += 1
			}
		}
	}

	for {
		flashes := grid.Flash()
		if len(flashes) == 0 {
			break
		}
		countFlashes += len(flashes)
	}

	for y := 0; y <= grid.maxY; y++ {
		for x := 0; x <= grid.maxX; x++ {
			if grid.values[y][x] > FlashLimit {
				grid.values[y][x] = ResetLimit
			}
		}
	}

	return countFlashes
}

func (grid *Grid) FindSync() int {
	countIteratons := 0
	for {
		grid.Step()
		countIteratons += 1
		if grid.FullReset() {
			return countIteratons
		}
	}
}

func (grid *Grid) Iterate(maxIterations int) int {
	countFlashes := 0
	for i := 0; i < maxIterations; i++ {
		countFlashes += grid.Step()
		// if i <= 10 || i%10 == 0 {
		// 	log.Println(i)
		// 	grid.Dump()
		// }
	}
	return countFlashes
}

func (grid *Grid) Dump() {
	log.Println()
	for y := 0; y <= grid.maxY; y++ {
		line := ""
		for x := 0; x <= grid.maxX; x++ {
			if grid.values[y][x] > FlashLimit {
				line += "X"
			} else {
				line += strconv.Itoa(grid.values[y][x])
			}
		}
		log.Println(line)
	}
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		var partOne *Grid = nil
		var partTwo *Grid = nil
		lineNUmber := 0
		for scanner.Scan() {
			inputSVs := strings.Split(scanner.Text(), "")
			if partOne == nil || partTwo == nil {
				partOne = new(Grid)
				partOne.Init(len(inputSVs), len(inputSVs))
				partTwo = new(Grid)
				partTwo.Init(len(inputSVs), len(inputSVs))
			}
			for x, sv := range inputSVs {
				iv, _ := strconv.Atoi(sv)
				partOne.Set(x, lineNUmber, iv)
				partTwo.Set(x, lineNUmber, iv)
			}
			lineNUmber++
		}
		inFile.Close()

		log.Println(partOne.Iterate(100))
		log.Print(partTwo.FindSync())
	}
}
