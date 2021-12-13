package main

import (
	"bufio"
	"log"
	"os"
	"strings"
)

func WalkOne(cave string, caveSystem map[string][]string, smallCaves map[string]bool, inWalk map[string]int) int {
	countWalks := 0
	if cave == "end" {
		countWalks = 1
	} else if smallCaves[cave] && inWalk[cave] > 0 {
		countWalks = 0
	} else {
		inWalk[cave]++
		for _, cn := range caveSystem[cave] {
			if cn != "start" {
				newWalk := make(map[string]int, len(inWalk))
				for k, v := range inWalk {
					newWalk[k] = v
				}
				countWalks += WalkOne(cn, caveSystem, smallCaves, newWalk)
			}
		}
	}
	return countWalks
}

func WalkTwo(cave string, freebieUsed bool, caveSystem map[string][]string, smallCaves map[string]bool, inWalk map[string]int) int {
	countWalks := 0

	if smallCaves[cave] && inWalk[cave] > 0 {
		if freebieUsed {
			countWalks = 0
		} else {
			inWalk[cave]++
			for _, cn := range caveSystem[cave] {
				if cn != "start" {
					newWalk := make(map[string]int, len(inWalk))
					for k, v := range inWalk {
						newWalk[k] = v
					}
					countWalks += WalkTwo(cn, true, caveSystem, smallCaves, newWalk)
				}
			}
		}
	} else if cave == "end" {
		countWalks++
	} else {
		inWalk[cave]++
		for _, cn := range caveSystem[cave] {
			if cn != "start" {
				newWalk := make(map[string]int, len(inWalk))
				for k, v := range inWalk {
					newWalk[k] = v
				}
				countWalks += WalkTwo(cn, freebieUsed, caveSystem, smallCaves, newWalk)
			}
		}
	}
	return countWalks
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		caveSystem := make(map[string][]string)
		smallCaves := make(map[string]bool)
		lineNUmber := 0
		for scanner.Scan() {
			inputSVs := strings.Split(scanner.Text(), "-")
			if len(inputSVs) != 2 {
				log.Panicln("impossible input:", inputSVs)
			}

			fromNode, toNode := inputSVs[0], inputSVs[1]
			if fromNode == "end" || toNode == "start" {
				tmp := fromNode
				fromNode = toNode
				toNode = tmp
			}

			caveSystem[fromNode] = append(caveSystem[fromNode], toNode)
			if fromNode != "start" && toNode != "end" {
				caveSystem[toNode] = append(caveSystem[toNode], fromNode)
				if toNode == strings.ToLower(toNode) {
					smallCaves[toNode] = true
				}
				if fromNode == strings.ToLower(fromNode) {
					smallCaves[fromNode] = true
				}
			}

			lineNUmber++
		}
		inFile.Close()

		walks := make(map[string]int)
		log.Println(WalkOne("start", caveSystem, smallCaves, walks))
		log.Println(WalkTwo("start", true, caveSystem, smallCaves, walks))
		log.Println(WalkTwo("start", false, caveSystem, smallCaves, walks))
	}
}
