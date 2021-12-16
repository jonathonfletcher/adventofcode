// This place is not a place of honor... no highly esteemed deed is commemorated here... nothing valued is here.
// What is here was dangerous and repulsive to us. This message is a warning about danger.
// The danger is still present, in your time, as it was in ours.
// The danger is to the mind, and it can kill.
// The form of the danger is an emanation of disgust.
// This place is best shunned and left uninhabited.
// https://en.wikipedia.org/wiki/Long-time_nuclear_waste_warning_messages

package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
)

type Node struct {
	x  int
	y  int
	td int
	c  int
	v  bool
}

type Grid struct {
	width  int
	height int
	values [][]*Node
}

func (grid *Grid) Init(width int, height int) {
	grid.width = width
	grid.height = height
	log.Printf("Init(%d,%d)", grid.height, grid.width)
	grid.values = make([][]*Node, grid.height)
	for y := 0; y < grid.height; y++ {
		grid.values[y] = make([]*Node, grid.width)
	}

}

func (grid *Grid) Set(x int, y int, n *Node) {
	// log.Printf("Set(%d,%d) = %+v", x, y, n)
	grid.values[y][x] = n
}

func (grid *Grid) Get(x int, y int) *Node {
	return grid.values[y][x]
}

func (grid *Grid) Neighbours(n *Node) []*Node {
	neighbours := make([]*Node, 0)
	for y := -1; y <= 1; y += 1 {
		for x := -1; x <= 1; x += 1 {
			if (x != 0 && y == 0) || (x == 0 && y != 0) {
				nx, ny := n.x+x, n.y+y
				if ny >= 0 && ny < grid.height && nx >= 0 && nx < grid.width {
					nn := grid.values[ny][nx]
					if !nn.v {
						neighbours = append(neighbours, nn)
					}
				}
			}
		}
	}
	return neighbours
}

func (grid *Grid) SDump() string {
	output := fmt.Sprintln()
	for y := 0; y < grid.height; y++ {
		line := ""
		for x := 0; x < grid.width; x++ {
			n := grid.values[y][x]
			line += fmt.Sprintf("%d", n.c)
		}
		output += fmt.Sprintln(line)
	}
	return output
}

func (grid *Grid) Walk(cn *Node, tgt *Node, i int) {

	for cn != tgt {
		for _, nn := range grid.Neighbours(cn) {
			if !nn.v {
				td := cn.td + nn.c
				if td < nn.td {
					nn.td = td
				}
			}
		}
		cn.v = true

		var smallest *Node = nil
		counter := 0
		for y := 0; y < grid.height; y++ {
			for x := 0; x < grid.width; x++ {
				n := grid.values[y][x]
				if !n.v {
					counter++
					if smallest == nil {
						smallest = n
					} else if n.td < smallest.td {
						smallest = n
					}
				}
			}
		}
		if counter%2500 == 0 {
			log.Println(counter)
		}
		cn = smallest
	}
	log.Print("----", *tgt, "----")
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	}
	defer inFile.Close()

	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanLines)

	y := 0
	var grid *Grid = nil
	var bigGrid *Grid = nil
	maxX, maxY := 0, 0
	bMaxX, bMaxY := 0, 0
	for scanner.Scan() {
		line := scanner.Text()
		if grid == nil {
			grid = new(Grid)
			maxX, maxY = len(line)-1, len(line)-1
			grid.Init(1+maxX, 1+maxY)
			log.Print(maxX, maxY)
		}
		if bigGrid == nil {
			bigGrid = new(Grid)
			bMaxX, bMaxY = (5*len(line))-1, (5*len(line))-1
			bigGrid.Init(1+bMaxX, 1+bMaxY)
			log.Print(bMaxX, bMaxY)
		}
		for x, sv := range line {
			c, _ := strconv.Atoi(string(sv))
			n := &Node{x: x, y: y, td: math.MaxInt, c: c}
			if x == 0 && y == 0 {
				n.td = 0
			}
			grid.Set(x, y, n)
			for mx := 0; mx < 5; mx++ {
				for my := 0; my < 5; my++ {
					bx := ((1 + maxX) * mx) + x
					by := ((1 + maxY) * my) + y
					bc := (((c + mx + my) - 1) % 9) + 1
					bn := &Node{x: bx, y: by, td: math.MaxInt, c: bc}
					if bx == 0 && by == 0 {
						bn.td = 0
					}
					bigGrid.Set(bx, by, bn)

				}
			}

		}
		y++
	}
	log.Print("----")
	grid.Walk(grid.Get(0, 0), grid.Get(maxX, maxY), 1)
	log.Printf("r:%d", grid.Get(maxX, maxY))

	log.Print("----")
	bigGrid.Walk(bigGrid.Get(0, 0), bigGrid.Get(bMaxX, bMaxY), 1)
	log.Printf("r:%d", bigGrid.Get(bMaxX, bMaxY))
}
