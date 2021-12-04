package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	GRIDSIZE = 5
)

const (
	NUMBERS int = iota
	GRIDS
)

type Grid struct {
	Values      [GRIDSIZE][GRIDSIZE]int64
	Called      [GRIDSIZE][GRIDSIZE]bool
	UnmarkedSum int64
}

func (grid *Grid) Reset() {
	grid.UnmarkedSum = 0
	for x, gRow := range grid.Called {
		for y, _ := range gRow {
			grid.Called[x][y] = false
			grid.UnmarkedSum += grid.Values[x][y]
		}
	}
}

func (grid *Grid) Call(n int64) bool {
	result := false
	for x, gRow := range grid.Values {
		for y, _ := range gRow {
			if grid.Values[x][y] == n && !grid.Called[x][y] {
				grid.Called[x][y] = true
				grid.UnmarkedSum -= n

				rc := true
				cc := true
				for i := 0; i < GRIDSIZE; i++ {
					if !grid.Called[i][y] {
						rc = false
					}
					if !grid.Called[x][i] {
						cc = false
					}
				}
				if rc || cc {
					result = true
				}
			}
		}
	}
	return result
}

func part1(numberList *[]int64, gridList *[]*Grid) int64 {

	for _, g := range *gridList {
		g.Reset()
	}

	for _, n := range *numberList {
		for _, g := range *gridList {
			called := g.Call(n)
			if called {
				return n * g.UnmarkedSum
			}
		}
	}
	return 0
}

func part2(numberList *[]int64, gridList *[]*Grid) int64 {

	for _, g := range *gridList {
		g.Reset()
	}

	calledGrids := make([]bool, len(*gridList))
	nCalledGrids := 0
	for i, _ := range *gridList {
		calledGrids[i] = false
	}

	for _, n := range *numberList {
		for gi, g := range *gridList {
			if !calledGrids[gi] {
				called := g.Call(n)
				if called {
					nCalledGrids++
					calledGrids[gi] = true
					if nCalledGrids == len(calledGrids) {
						return n * g.UnmarkedSum
					}
				}
			}
		}
	}
	return 0
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		var numberList []int64 = nil
		var gridList []*Grid = nil
		var grid *Grid
		gridRow := 0
		scannerState := NUMBERS
		for scanner.Scan() {
			line := scanner.Text()
			if len(line) == 0 {
				switch scannerState {
				case NUMBERS:
					scannerState = GRIDS
				case GRIDS:
					gridList = append(gridList, grid)
				}
				grid = new(Grid)
				gridRow = 0
				continue
			}
			switch scannerState {
			case NUMBERS:
				parts := strings.Split(line, ",")
				for _, v := range parts {
					i, _ := strconv.ParseInt(v, 10, 32)
					numberList = append(numberList, i)
				}
			case GRIDS:
				rowValues := strings.Fields(line)
				for i, v := range rowValues {
					v, _ := strconv.ParseInt(v, 10, 32)
					grid.Values[gridRow][i] = v
					grid.UnmarkedSum += v
				}
				gridRow++
			default:
			}
		}
		inFile.Close()
		gridList = append(gridList, grid)

		p1 := part1(&numberList, &gridList)
		log.Println("part1:", p1)
		p2 := part2(&numberList, &gridList)
		log.Println("part1:", p2)

	}
}
