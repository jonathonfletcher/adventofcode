package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func countTheFish(counters *[10]int64, nDays int) int64 {

	var lCounters [10]int64
	for i, v := range *counters {
		lCounters[i] = v
	}

	i0 := 0
	iR := 7
	iN := 9
	modVal := len(lCounters)
	for x := 0; x < nDays; x++ {
		lCounters[iR] += lCounters[i0]
		lCounters[iN] = lCounters[i0]
		lCounters[i0] = 0

		i0 = (i0 + 1) % modVal
		iR = (iR + 1) % modVal
		iN = (iN + 1) % modVal
	}

	// log.Println(i0, lCounters)
	var sum int64 = 0
	for _, v := range lCounters {
		sum += v
	}
	return sum
}

func main() {

	inFile, err := os.Open("part0.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		var counters [10]int64
		for scanner.Scan() {
			line := scanner.Text()

			lineValues := strings.Split(line, ",")
			log.Println("line:", lineValues)
			for _, sv := range lineValues {
				iv, _ := strconv.ParseInt(sv, 10, 32)
				counters[iv] += 1
			}
		}
		inFile.Close()

		log.Println(counters)
		log.Print(countTheFish(&counters, 18))
		log.Print("part1:", countTheFish(&counters, 80))
		log.Print("part2:", countTheFish(&counters, 256))

	}
}
