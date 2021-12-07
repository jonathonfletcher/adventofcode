package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func crabbingCost(counters *[]int64, moveCosts *[]int64) int64 {

	// minCandidate := 0
	var minMoveCost int64 = int64(len(*counters) * int((*moveCosts)[len(*counters)]))
	for candidate := 0; candidate < len(*counters); candidate++ {
		var candidateMoveCost int64 = 0
		for x := 0; x < len(*counters); x++ {
			xDiff := x - candidate
			if xDiff < 0 {
				xDiff *= -1
			}
			if xDiff != 0 {
				candidateMoveCost += (*counters)[x] * (*moveCosts)[xDiff]
			}
		}
		// log.Println(candidate, candidateMoveCost)
		if candidateMoveCost <= minMoveCost {
			minMoveCost = candidateMoveCost
			// minCandidate = candidate
		}
	}
	// log.Println(minCandidate, minMoveCost)
	return minMoveCost
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		counters := make([]int64, 0)
		n := 0
		for scanner.Scan() {
			lineValues := strings.Split(scanner.Text(), ",")
			// log.Println("line:", lineValues)
			for _, sv := range lineValues {
				iv, _ := strconv.ParseInt(sv, 10, 32)
				if iv >= int64(len(counters)) {
					t := make([]int64, iv+1)
					copy(t, counters)
					counters = t
				}
				counters[iv] += 1
				n += 1
			}
		}
		inFile.Close()

		partOneFuelCost := make([]int64, len(counters)+1)
		partTwoFuelCost := make([]int64, len(counters)+1)
		for i := 1; i <= len(counters); i++ {
			partOneFuelCost[i] = int64(i)
			partTwoFuelCost[i] = int64(i) + partTwoFuelCost[i-1]
		}

		log.Println("part1", crabbingCost(&counters, &partOneFuelCost))
		log.Println("part2", crabbingCost(&counters, &partTwoFuelCost))
	}
}
