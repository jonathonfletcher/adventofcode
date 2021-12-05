package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Edge struct {
	x1 int64
	y1 int64
	x2 int64
	y2 int64
}

func doCountingThingInUglyProceduralForm(edges *[]*Edge, partTwo bool) int {
	counter := 0
	grid := make(map[string]int)

	for _, e := range *edges {
		x := e.x1
		ex := e.x2
		var dx int64 = 1
		if x > ex {
			dx = -1
		} else if x == ex {
			dx = 0
		}
		ex += dx

		y := e.y1
		ey := e.y2
		var dy int64 = 1
		if y > ey {
			dy = -1
		} else if y == ey {
			dy = 0
		}
		ey += dy

		// log.Println(e.x1, e.y1, " -> ", e.x2, e.y2)
		// log.Println(x, ex, dx, " -> ", y, ey, dy)
		for {
			if x == ex && y == ey {
				break
			}
			k := fmt.Sprintf("%d,%d", x, y)
			v := grid[k]
			// log.Println(k, ":", v, p)
			isHV := dx == 0 || dy == 0
			if partTwo || isHV {
				v += 1
				if v == 2 {
					counter++
				}
				grid[k] = v
			}
			x += dx
			y += dy
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

		var edges []*Edge

		for scanner.Scan() {
			line := scanner.Text()
			rowValues := strings.Fields(line)
			if len(rowValues) != 3 {
				log.Panicln("invalid: ", line)
				continue
			}

			p1 := strings.Split(rowValues[0], ",")
			x1, _ := strconv.ParseInt(p1[0], 10, 32)
			y1, _ := strconv.ParseInt(p1[1], 10, 32)

			p2 := strings.Split(rowValues[2], ",")
			x2, _ := strconv.ParseInt(p2[0], 10, 32)
			y2, _ := strconv.ParseInt(p2[1], 10, 32)

			edges = append(edges, &Edge{x1, y1, x2, y2})
		}
		inFile.Close()

		log.Println("part1:", doCountingThingInUglyProceduralForm(&edges, false))
		log.Println("part2:", doCountingThingInUglyProceduralForm(&edges, true))

	}
}
