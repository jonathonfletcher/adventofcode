package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Dot struct {
	x int
	y int
}

type Fold struct {
	axis   int
	offset int
}

type Grid struct {
	width  int
	height int
	values [][]bool
}

func (grid *Grid) Init(width int, height int) {
	grid.width = width
	grid.height = height
	grid.values = make([][]bool, grid.height)
	for y := 0; y < grid.height; y++ {
		grid.values[y] = make([]bool, grid.width)
	}
}

func (grid *Grid) Set(x int, y int, v bool) {
	grid.values[y][x] = v
}

func (grid *Grid) Get(x int, y int) bool {

	return grid.values[y][x]
}

func (grid *Grid) Dump(limX int, limY int) string {
	output := fmt.Sprintln()
	for y := 0; y < limY && y < grid.height; y++ {
		line := ""
		for x := 0; x < limX && x < grid.width; x++ {
			switch grid.Get(x, y) {
			case true:
				line += "#"
			default:
				line += "."
			}
		}
		output += fmt.Sprintln(line)
	}
	return output
}

func (grid *Grid) CountVisible() int {
	counter := 0
	for y := 0; y < grid.height; y++ {
		for x := 0; x < grid.width; x++ {
			if grid.values[y][x] {
				counter++
			}
		}
	}
	return counter
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		limX := 0
		limY := 0
		dotList := make([]*Dot, 0)
		foldList := make([]*Fold, 0)
		lineNUmber := 0
		readingDots := true
		for scanner.Scan() {
			line := scanner.Text()
			lineNUmber++

			if len(line) == 0 {
				if readingDots {
					readingDots = !readingDots
				}
				continue
			} else {
				// log.Println(line)
				if readingDots {
					dot := new(Dot)
					if n, _ := fmt.Sscanf(line, "%d,%d", &dot.x, &dot.y); n != 2 {
						log.Panicln("impossible input:", line)
					}
					if dot.x > limX {
						limX = dot.x
					}
					if dot.y > limY {
						limY = dot.y
					}
					dotList = append(dotList, dot)
				} else {
					var foldAxis rune
					var foldOffset int
					if n, _ := fmt.Sscanf(line, "fold along %c=%d", &foldAxis, &foldOffset); n != 2 {
						log.Panicln("impossible input:", line)
					}
					fold := new(Fold)
					fold.offset = foldOffset
					switch foldAxis {
					case 'x':
						fold.axis = 0
					case 'y':
						fold.axis = 1
					}
					foldList = append(foldList, fold)
					// log.Printf("%c %d", foldAxis, foldOffset)
				}
			}
		}
		inFile.Close()

		// log.Println(limX, limY)
		limX, limY = 1+limX, 1+limY

		grid := new(Grid)
		grid.Init(limX, limY)

		for _, p := range dotList {
			grid.Set(p.x, p.y, true)
		}
		// log.Print(grid.Dump(limX, limY))

		limX, limY = grid.width, grid.height
		// log.Print(grid.Dump(limX, limY))
		printedFirst := false

		for _, f := range foldList {
			// log.Printf("%d %d ( %d, %d )", f.axis, f.offset, grid.width, grid.height)
			switch f.axis {
			case 0:
				for fx := f.offset + 1; fx < limX && fx < grid.width; fx++ {
					tx := f.offset + f.offset - fx
					// log.Printf("%d -> %d", fx, tx)
					for y := 0; y < limY && y < grid.height; y++ {
						grid.Set(tx, y, grid.Get(tx, y) || grid.Get(fx, y))
						grid.Set(fx, y, false)
					}
					if tx <= 0 {
						break
					}
				}
				if f.offset < limX {
					limX = f.offset
				}
			case 1:
				for fy := f.offset + 1; fy < limY && fy < grid.height; fy++ {
					ty := f.offset + f.offset - fy
					// log.Printf("%d -> %d", fy, ty)
					for x := 0; x < limX && x < grid.width; x++ {
						grid.Set(x, ty, grid.Get(x, ty) || grid.Get(x, fy))
						grid.Set(x, fy, false)
					}
					if ty <= 0 {
						break
					}
				}
				if f.offset < limY {
					limY = f.offset
				}
			}
			if !printedFirst {
				printedFirst = true
				// log.Print(grid.Dump(limX, limY))
				log.Println(grid.CountVisible())
			}
		}
		log.Print(grid.Dump(limX, limY))
		// log.Println(grid.CountVisible())
	}
}
