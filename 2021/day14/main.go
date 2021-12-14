package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		var template string
		mappingRules := make(map[string]rune)
		lineNUmber := 0
		readingPolymer := true
		for scanner.Scan() {
			line := scanner.Text()
			lineNUmber++

			if len(line) == 0 {
				if readingPolymer {
					readingPolymer = !readingPolymer
				}
				continue
			} else {
				if readingPolymer {
					template = line
				} else {
					var mapFrom string
					var mapTo rune
					if n, _ := fmt.Sscanf(line, "%s -> %c", &mapFrom, &mapTo); n != 2 {
						log.Panicln("impossible input:", line, n)
					}
					mappingRules[mapFrom] = mapTo
				}
			}
		}
		inFile.Close()

		bruteForce := false
		if bruteForce {
			for i := 0; i < 10; i++ {
				newTemplate := ""
				var pv rune
				for i, v := range template {
					if i == 0 {
						newTemplate += string(v)
					} else {
						k := string(pv) + string(v)
						if mk, ok := mappingRules[k]; ok {
							newTemplate += string(mk)
						}
						newTemplate += string(v)
					}
					pv = v
				}
				template = newTemplate
			}

			{
				counterMap := make(map[rune]int)
				for _, v := range template {
					counterMap[v]++
				}
				var maxV int = 0
				var minV int = -1
				for _, v := range counterMap {
					if v > 0 {
						if v > maxV {
							maxV = v
						}
						if v < minV || minV < 0 {
							minV = v
						}
					}
				}
				log.Printf("%d - %d = %d", maxV, minV, maxV-minV)
			}

		} else {
			templateEndsPair := string(template[0]) + string(template[len(template)-1])
			templatePairs := make(map[string]int)
			for i, _ := range template {
				if i > 0 {
					pair := string(template[i-1]) + string(template[i])
					// += 1 ... the pair may be present more than once ..
					templatePairs[pair] += 1
				}
			}
			log.Println(templatePairs)

			for i := 0; i < 40; i++ {

				newTemplatePairs := make(map[string]int)
				for k, v := range templatePairs {
					if c, ok := mappingRules[k]; ok {
						ls := string(k[0]) + string(c)
						rs := string(c) + string(k[1])
						newTemplatePairs[ls] += v
						newTemplatePairs[rs] += v
					}
				}
				templatePairs = newTemplatePairs

				{
					counterMap := make(map[byte]int)
					counterMap[templateEndsPair[0]] += 1
					counterMap[templateEndsPair[1]] += 1
					for k, v := range templatePairs {
						counterMap[k[0]] += v
						counterMap[k[1]] += v
					}
					// we double-counted everything.
					// what if it isn't an even number?
					for k, v := range counterMap {
						counterMap[k] = v / 2
					}

					var maxV int = 0
					var minV int = -1
					for _, v := range counterMap {
						if v > 0 {
							if v > maxV {
								maxV = v
							}
							if v < minV || minV < 0 {
								minV = v
							}
						}
					}

					log.Printf("%d : %d - %d = %d", 1+i, maxV, minV, maxV-minV)
				}

			}
		}
	}
}
